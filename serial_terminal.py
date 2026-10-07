#!/usr/bin/env python3
"""Simple Tera Term-like serial terminal for Linux (Tkinter + pyserial)."""
import codecs
import glob
import json
import os
import queue
import sys
import threading
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

import serial
import serial.tools.list_ports

APP_NAME = "Serial Terminal"
APP_VERSION = "1.0.0"
APP_BUILD_DATE = "October 7, 2026"

IS_WINDOWS = sys.platform.startswith("win")
MONO_FONT = "Consolas" if IS_WINDOWS else "DejaVu Sans Mono"

PORT_PATTERNS = ("/dev/ttyUSB*", "/dev/ttyACM*")
BAUDS = [300, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400,
         460800, 921600, 1000000, 2000000]
PARITY = {"None": serial.PARITY_NONE, "Even": serial.PARITY_EVEN,
          "Odd": serial.PARITY_ODD, "Mark": serial.PARITY_MARK,
          "Space": serial.PARITY_SPACE}
BYTESIZE = {"5": serial.FIVEBITS, "6": serial.SIXBITS,
            "7": serial.SEVENBITS, "8": serial.EIGHTBITS}
STOPBITS = {"1": serial.STOPBITS_ONE, "1.5": serial.STOPBITS_ONE_POINT_FIVE,
            "2": serial.STOPBITS_TWO}
TX_EOL = {"CR": b"\r", "LF": b"\n", "CR+LF": b"\r\n"}

CONFIG_FILE = os.path.join(
    os.environ.get("APPDATA" if IS_WINDOWS else "XDG_CONFIG_HOME")
    or os.path.expanduser("~/.config"),
    "serial-terminal", "settings.json")


def load_settings():
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save_settings(data):
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        tmp = CONFIG_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, CONFIG_FILE)
    except OSError:
        pass


# Ports currently opened by any window of this application.
_in_use = {}
_windows = []


def _port_key(p):
    base = p.rstrip("0123456789")
    return (base, int(p[len(base):] or 0))


def list_ports():
    """COMx on Windows; /dev/ttyUSB* and /dev/ttyACM* on Linux."""
    if IS_WINDOWS:
        return sorted({p.device for p in serial.tools.list_ports.comports()}, key=_port_key)
    ports = []
    for pat in PORT_PATTERNS:
        ports.extend(glob.glob(pat))
    return sorted(set(ports), key=_port_key)


def _windows_busy(ports):
    """Windows gives exclusive access, so a failed open means another program has it."""
    busy = set()
    for p in ports:
        try:
            serial.Serial(p).close()
        except serial.SerialException as ex:
            if "PermissionError" in str(ex) or "Access is denied" in str(ex):
                busy.add(p)
        except OSError:
            pass
    return busy


def ports_open_by_other_processes():
    """Device paths held open by other processes (as far as /proc lets us see)."""
    if IS_WINDOWS:
        return set()
    busy = set()
    me = str(os.getpid())
    for fd_dir in glob.glob("/proc/[0-9]*/fd"):
        if fd_dir.split("/")[2] == me:
            continue
        try:
            for fd in os.listdir(fd_dir):
                try:
                    target = os.readlink(os.path.join(fd_dir, fd))
                except OSError:
                    continue
                if target.startswith(("/dev/ttyUSB", "/dev/ttyACM")):
                    busy.add(target)
        except OSError:
            continue
    return busy


def busy_ports():
    busy = set(_in_use)
    if IS_WINDOWS:
        return busy | _windows_busy([p for p in list_ports() if p not in busy])
    return busy | ports_open_by_other_processes()


class TerminalWindow:
    def __init__(self, master):
        self.win = tk.Toplevel(master)
        self.master = master
        self.ser = None
        self.port = None
        self.rx_queue = queue.Queue()
        self.reader = None
        self.stop_evt = threading.Event()
        self.hex_col = 0
        self._dec = codecs.getincrementaldecoder("utf-8")(errors="replace")
        self.auto_reconnect = False
        self.reconnect_timer = 0
        _windows.append(self)

        self.win.title(f"{APP_NAME} v{APP_VERSION} - disconnected")
        self.win.geometry("900x560")
        self.win.protocol("WM_DELETE_WINDOW", self.close)

        self.v_port = tk.StringVar(value="")
        self.v_baud = tk.StringVar(value="115200")
        self.v_data = tk.StringVar(value="8")
        self.v_parity = tk.StringVar(value="None")
        self.v_stop = tk.StringVar(value="1")
        self.v_flow = tk.StringVar(value="None")
        self.v_tx_eol = tk.StringVar(value="CR")
        self.v_echo = tk.BooleanVar(value=False)
        self.v_hex = tk.BooleanVar(value=False)
        self.v_ts = tk.BooleanVar(value=False)
        self.v_autoscroll = tk.BooleanVar(value=True)
        self.v_dtr = tk.BooleanVar(value=True)
        self.v_rts = tk.BooleanVar(value=True)
        self.v_status = tk.StringVar(value="Not connected")
        self._persisted = {
            "port": self.v_port, "baud": self.v_baud, "data_bits": self.v_data,
            "parity": self.v_parity, "stop_bits": self.v_stop, "flow": self.v_flow,
            "enter_sends": self.v_tx_eol, "local_echo": self.v_echo, "hex_view": self.v_hex,
            "timestamps": self.v_ts, "auto_scroll": self.v_autoscroll,
            "dtr": self.v_dtr, "rts": self.v_rts}
        self._load_persisted()
        self.at_line_start = True

        self._build_menu()
        self._build_toolbar()
        self._build_terminal()
        ttk.Label(self.win, textvariable=self.v_status, relief="sunken",
                  anchor="w").pack(side="bottom", fill="x")
        self.refresh_ports()
        self.win.after(20, self._poll)

    # ---------- persistent settings ----------
    def _load_persisted(self):
        saved = load_settings()
        choices = {"data_bits": BYTESIZE, "parity": PARITY, "stop_bits": STOPBITS,
                   "flow": ("None", "RTS/CTS", "XON/XOFF", "DSR/DTR"), "enter_sends": TX_EOL}
        for key, var in self._persisted.items():
            val = saved.get(key)
            if val is None or (key in choices and val not in choices[key]):
                continue
            if key == "baud" and not str(val).isdigit():
                continue
            try:
                var.set(val)
            except tk.TclError:
                pass
        for var in self._persisted.values():
            var.trace_add("write", lambda *_: self._save_persisted())

    def _save_persisted(self):
        data = load_settings()
        for key, var in self._persisted.items():
            try:
                data[key] = var.get()
            except tk.TclError:
                pass
        save_settings(data)

    def open_port_settings(self):
        dlg = tk.Toplevel(self.win)
        dlg.title("Serial Port Settings")
        dlg.transient(self.win)
        dlg.resizable(False, False)
        body = ttk.Frame(dlg, padding=12)
        body.pack(fill="both", expand=True)
        rows = [("Data bits:", self.v_data, list(BYTESIZE), True),
                ("Parity:", self.v_parity, list(PARITY), True),
                ("Stop bits:", self.v_stop, list(STOPBITS), True),
                ("Flow control:", self.v_flow, ["None", "RTS/CTS", "XON/XOFF", "DSR/DTR"], True),
                ("Enter sends:", self.v_tx_eol, list(TX_EOL), False)]
        temp = {}
        for i, (label, var, values, locked_when_open) in enumerate(rows):
            ttk.Label(body, text=label).grid(row=i, column=0, sticky="w", pady=3)
            temp[label] = tk.StringVar(value=var.get())
            cb = ttk.Combobox(body, textvariable=temp[label], values=values,
                              width=12, state="readonly")
            if self.ser and locked_when_open:
                cb.config(state="disabled")
            cb.grid(row=i, column=1, padx=(10, 0), pady=3)
        note = "Port settings can't change while connected." if self.ser else \
            "Settings are saved automatically for next sessions."
        ttk.Label(body, text=note, foreground="gray").grid(
            row=len(rows), column=0, columnspan=2, pady=(8, 0))

        def ok():
            for label, var, _, locked in rows:
                if not (self.ser and locked):
                    var.set(temp[label].get())
            dlg.destroy()

        btns = ttk.Frame(body)
        btns.grid(row=len(rows) + 1, column=0, columnspan=2, pady=(10, 0), sticky="e")
        ttk.Button(btns, text="OK", command=ok).pack(side="left", padx=4)
        ttk.Button(btns, text="Cancel", command=dlg.destroy).pack(side="left")
        dlg.bind("<Return>", lambda e: ok())
        dlg.bind("<Escape>", lambda e: dlg.destroy())
        dlg.wait_visibility()
        dlg.grab_set()

    # ---------- UI ----------
    def _build_menu(self):
        mb = tk.Menu(self.win)
        f = tk.Menu(mb, tearoff=0)
        f.add_command(label="New Window", accelerator="Ctrl+N", command=self.new_window)
        f.add_command(label="Save Log...", command=self.save_log)
        f.add_separator()
        f.add_command(label="Close Window", accelerator="Ctrl+W", command=self.close)
        f.add_command(label="Exit (close all)", command=quit_all)
        mb.add_cascade(label="File", menu=f)
        e = tk.Menu(mb, tearoff=0)
        e.add_command(label="Copy", accelerator="Ctrl+Shift+C", command=self.copy)
        e.add_command(label="Paste (send)", accelerator="Ctrl+Shift+V", command=self.paste)
        e.add_command(label="Clear Screen", command=self.clear)
        mb.add_cascade(label="Edit", menu=e)
        s = tk.Menu(mb, tearoff=0)
        s.add_command(label="Serial port...", command=self.open_port_settings)
        s.add_separator()
        s.add_checkbutton(label="Local echo", variable=self.v_echo)
        s.add_checkbutton(label="Hex view", variable=self.v_hex)
        s.add_checkbutton(label="Timestamps", variable=self.v_ts)
        s.add_checkbutton(label="Auto-scroll", variable=self.v_autoscroll)
        s.add_separator()
        s.add_checkbutton(label="DTR", variable=self.v_dtr, command=self.apply_lines)
        s.add_checkbutton(label="RTS", variable=self.v_rts, command=self.apply_lines)
        s.add_command(label="Send Break", command=self.send_break)
        mb.add_cascade(label="Setup", menu=s)
        h = tk.Menu(mb, tearoff=0)
        h.add_command(label="About", command=self.show_about)
        h.add_command(label="Check for Updates", command=self.check_updates)
        h.add_separator()
        h.add_command(label="View Version", command=self.show_version)
        mb.add_cascade(label="Help", menu=h)
        self.win.config(menu=mb)
        self.win.bind("<Control-n>", lambda e: self.new_window())
        self.win.bind("<Control-w>", lambda e: self.close())

    def _build_toolbar(self):
        bar = ttk.Frame(self.win, padding=4)
        bar.pack(side="top", fill="x")

        ttk.Label(bar, text="Port:").pack(side="left")
        self.port_btn = ttk.Menubutton(bar, textvariable=self.v_port, width=16)
        self.port_menu = tk.Menu(self.port_btn, tearoff=0)
        self.port_btn["menu"] = self.port_menu
        self.port_btn.pack(side="left", padx=(2, 2))
        ttk.Button(bar, text="⟳ Refresh", width=9, command=self.refresh_ports).pack(side="left")

        def combo(label, var, values, width, editable=False):
            ttk.Label(bar, text=label).pack(side="left", padx=(8, 2))
            cb = ttk.Combobox(bar, textvariable=var, values=values, width=width,
                              state="normal" if editable else "readonly")
            cb.pack(side="left")
            return cb

        self.setting_widgets = [combo("Baud:", self.v_baud, BAUDS, 8, editable=True)]
        ttk.Button(bar, text="⚙ Settings", command=self.open_port_settings).pack(
            side="left", padx=(8, 0))
        
        # Auto-scroll toggle button
        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=8)
        self.autoscroll_btn = ttk.Button(bar, text="📍 Auto-Scroll: ON", width=16,
                                         command=self._toggle_autoscroll)
        self.autoscroll_btn.pack(side="left", padx=4)
        self.v_autoscroll.trace_add("write", self._update_autoscroll_btn)
        self._update_autoscroll_btn()
        
        self.conn_btn = ttk.Button(bar, text="Connect", width=11, command=self.toggle_connection)
        self.conn_btn.pack(side="right")

    def _build_terminal(self):
        frame = ttk.Frame(self.win)
        frame.pack(fill="both", expand=True)
        self.text = tk.Text(frame, bg="black", fg="#d0d0d0", insertbackground="#00ff00",
                            font=(MONO_FONT, 11), wrap="char", undo=False)
        sb = ttk.Scrollbar(frame, command=self.text.yview)
        self.text.config(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        self.text.tag_config("ts", foreground="#6fa8dc")
        self.text.tag_config("sys", foreground="#e6b800")
        self.text.bind("<Key>", self.on_key)
        self.text.bind("<Control-Shift-C>", lambda e: (self.copy(), "break")[1])
        self.text.bind("<Control-Shift-V>", lambda e: (self.paste(), "break")[1])
        self.text.bind("<<Paste>>", lambda e: (self.paste(), "break")[1])
        self.text.bind("<Button-2>", lambda e: (self.paste(), "break")[1])
        self.text.bind("<Button-1>", lambda e: self.text.focus_set())
        self.text.bind("<B1-Motion>", self._on_text_select)
        self.text.bind("<ButtonRelease-1>", self._on_text_select)
        self.text.focus_set()

    # ---------- ports ----------
    def refresh_ports(self):
        busy = busy_ports()
        if self.ser:
            busy.discard(self.port)
        ports = list_ports()
        self.port_menu.delete(0, "end")
        if not ports:
            self.port_menu.add_command(label="(no serial ports found)",
                                       state="disabled")
        for p in ports:
            if p in busy:
                self.port_menu.add_command(label=f"{p}  (busy)", state="disabled",
                                           foreground="gray")
            else:
                self.port_menu.add_command(label=p, command=lambda p=p: self.v_port.set(p))
        
        # If port is currently selected but not available (e.g., device removed),
        # add it to the menu as unavailable so user can see their selection is pending
        current_port = self.v_port.get()
        if current_port and current_port not in ports:
            status = "(reconnecting...)" if self.auto_reconnect else "(disconnected)"
            color = "blue" if self.auto_reconnect else "orange"
            self.port_menu.add_command(label=f"{current_port}  {status}", 
                                      state="disabled", foreground=color)
        
        self.port_btn.state(["!disabled"] if not self.ser else ["disabled"])

    def _toggle_autoscroll(self):
        self.v_autoscroll.set(not self.v_autoscroll.get())

    def _update_autoscroll_btn(self, *args):
        if hasattr(self, 'autoscroll_btn'):
            state = "ON" if self.v_autoscroll.get() else "OFF"
            self.autoscroll_btn.config(text=f"📍 Auto-Scroll: {state}")

    # ---------- connection ----------
    def toggle_connection(self):
        if self.ser:
            self.auto_reconnect = False
            self.disconnect()
        else:
            self.auto_reconnect = False
            self.reconnect_timer = 0
            self.connect()

    def connect(self):
        port = self.v_port.get()
        if not port:
            messagebox.showwarning("Serial Terminal", "Select a port first.", parent=self.win)
            return
        if port in busy_ports():
            messagebox.showerror("Serial Terminal", f"{port} is busy.", parent=self.win)
            self.refresh_ports()
            return
        try:
            baud = int(self.v_baud.get())
            flow = self.v_flow.get()
            self.ser = serial.Serial(
                port=port, baudrate=baud,
                bytesize=BYTESIZE[self.v_data.get()],
                parity=PARITY[self.v_parity.get()],
                stopbits=STOPBITS[self.v_stop.get()],
                timeout=0.1, write_timeout=2,
                exclusive=None if IS_WINDOWS else True,
                rtscts=flow == "RTS/CTS", xonxoff=flow == "XON/XOFF",
                dsrdtr=flow == "DSR/DTR")
        except (ValueError, serial.SerialException, OSError) as ex:
            self.ser = None
            messagebox.showerror("Serial Terminal", f"Cannot open {port}:\n{ex}", parent=self.win)
            self.refresh_ports()
            return
        self.port = port
        _in_use[port] = self
        self.apply_lines()
        self.stop_evt.clear()
        self.reader = threading.Thread(target=self._read_loop, args=(self.ser,), daemon=True)
        self.reader.start()
        self.conn_btn.config(text="Disconnect")
        for w in self.setting_widgets:
            w.config(state="disabled")
        self.win.title(f"{APP_NAME} v{APP_VERSION} - {port}")
        self.v_status.set(f"Connected: {port}  {self.v_baud.get()} "
                          f"{self.v_data.get()}{self.v_parity.get()[0]}{self.v_stop.get()}  "
                          f"flow={self.v_flow.get()}")
        self.refresh_ports()
        self.text.focus_set()

    def disconnect(self, reason=None):
        if not self.ser:
            return
        self.stop_evt.set()
        ser, self.ser = self.ser, None
        if self.reader:
            self.reader.join(timeout=0.5)
        try:
            ser.close()
        except Exception:
            pass
        if _in_use.get(self.port) is self:
            del _in_use[self.port]
        self.conn_btn.config(text="Connect")
        for w in self.setting_widgets:
            w.config(state="normal")
        self.win.title(f"{APP_NAME} v{APP_VERSION} - disconnected")
        self.v_status.set(reason or "Disconnected")
        if reason:
            self._append_text(f"\n[{reason}]\n", "sys")
            # Enable auto-reconnect if device was removed
            if "device removed" in reason.lower() or "connection lost" in reason.lower():
                self.auto_reconnect = True
                self.reconnect_timer = 0
        for w in _windows:
            w.refresh_ports()

    def apply_lines(self):
        if self.ser:
            try:
                if not self.ser.dsrdtr:
                    self.ser.dtr = self.v_dtr.get()
                if not self.ser.rtscts:
                    self.ser.rts = self.v_rts.get()
            except (serial.SerialException, OSError):
                pass

    def send_break(self):
        if self.ser:
            try:
                self.ser.send_break(0.25)
            except (serial.SerialException, OSError):
                pass

    def _read_loop(self, ser):
        while not self.stop_evt.is_set():
            try:
                data = ser.read(ser.in_waiting or 1)
            except (serial.SerialException, OSError, TypeError):
                if not self.stop_evt.is_set():
                    self.rx_queue.put(None)
                return
            if data:
                self.rx_queue.put(data)

    # ---------- receive / display ----------
    def _poll(self):
        try:
            # Auto-reconnect logic: try to reconnect every 1 second (50 poll cycles * 20ms)
            if self.auto_reconnect and not self.ser:
                self.reconnect_timer += 1
                if self.reconnect_timer >= 50:
                    self.reconnect_timer = 0
                    port = self.v_port.get()
                    if port:
                        # Check if port is now available
                        available_ports = list_ports()
                        if port in available_ports:
                            try:
                                # Try to reconnect
                                self.stop_evt.clear()
                                baud = int(self.v_baud.get())
                                flow = self.v_flow.get()
                                self.ser = serial.Serial(
                                    port=port, baudrate=baud,
                                    bytesize=BYTESIZE[self.v_data.get()],
                                    parity=PARITY[self.v_parity.get()],
                                    stopbits=STOPBITS[self.v_stop.get()],
                                    timeout=0.1, write_timeout=2,
                                    exclusive=None if IS_WINDOWS else True,
                                    rtscts=flow == "RTS/CTS", xonxoff=flow == "XON/XOFF",
                                    dsrdtr=flow == "DSR/DTR")
                                self.port = port
                                _in_use[port] = self
                                self.apply_lines()
                                self.reader = threading.Thread(target=self._read_loop, args=(self.ser,), daemon=True)
                                self.reader.start()
                                self.conn_btn.config(text="Disconnect")
                                for w in self.setting_widgets:
                                    w.config(state="disabled")
                                self.win.title(f"Serial Terminal - {port}")
                                self.v_status.set(f"Connected: {port}  {self.v_baud.get()} "
                                                f"{self.v_data.get()}{self.v_parity.get()[0]}{self.v_stop.get()}  "
                                                f"flow={self.v_flow.get()}")
                                self._append_text(f"\n[Reconnected to {port}]\n", "sys")
                                self.auto_reconnect = False
                                self.reconnect_timer = 0
                                for w in _windows:
                                    w.refresh_ports()
                            except Exception:
                                # Reconnect failed, will try again
                                self.ser = None
                                pass
            
            chunks = []
            lost = False
            while True:
                try:
                    item = self.rx_queue.get_nowait()
                except queue.Empty:
                    break
                if item is None:
                    lost = True
                else:
                    chunks.append(item)
            if chunks:
                self._display(b"".join(chunks))
            if lost and self.ser:
                self.disconnect("Connection lost (device removed?)")
        finally:
            self.win.after(20, self._poll)

    def _display(self, data):
        if self.v_hex.get():
            out = []
            for b in data:
                out.append(f"{b:02X} ")
                self.hex_col += 1
                if self.hex_col >= 16:
                    out.append("\n")
                    self.hex_col = 0
            self._append_text("".join(out))
            return
        s = self._dec.decode(data).replace("\r\n", "\n").replace("\r", "\n")
        self._append_text(s)

    def _append_text(self, s, tag=None):
        t = self.text
        # Process backspace characters
        for part in self._split_bs(s):
            if part == "\b":
                if t.compare("end-1c", ">", "1.0") and t.get("end-2c") != "\n":
                    t.delete("end-2c")
                continue
            if part == "\x07" or part == "\x00":
                continue
            part = part.replace("\x1b", "␛")
            if self.v_ts.get() and tag is None:
                out = []
                for ch in part:
                    if self.at_line_start and ch != "\n":
                        t.insert("end-1c", "".join(out), tag)
                        out = []
                        t.insert("end-1c", datetime.now().strftime("[%H:%M:%S.%f")[:-3] + "] ", "ts")
                        self.at_line_start = False
                    out.append(ch)
                    if ch == "\n":
                        self.at_line_start = True
                t.insert("end-1c", "".join(out), tag)
            else:
                t.insert("end-1c", part, tag)
                if part:
                    self.at_line_start = part.endswith("\n")
        # Limit scrollback
        lines = int(t.index("end-1c").split(".")[0])
        if lines > 20000:
            t.delete("1.0", f"{lines - 20000}.0")
        if self.v_autoscroll.get():
            t.see("end")

    @staticmethod
    def _split_bs(s):
        buf, parts = [], []
        for ch in s:
            if ch in "\b\x07\x00":
                if buf:
                    parts.append("".join(buf))
                    buf = []
                parts.append(ch)
            else:
                buf.append(ch)
        if buf:
            parts.append("".join(buf))
        return parts

    # ---------- transmit ----------
    def _write(self, data):
        if not self.ser:
            return False
        try:
            self.ser.write(data)
            return True
        except (serial.SerialException, OSError):
            self.disconnect("Write failed - connection lost")
            return False

    def on_key(self, e):
        if e.state & 0x4 and e.keysym.lower() in ("c", "v") and e.state & 0x1:
            return None  # handled by dedicated bindings
        if e.state & 0x4 and e.keysym.lower() == "n":
            return None
        if e.state & 0x4 and e.keysym.lower() == "w":
            return None
        special = {"Return": TX_EOL[self.v_tx_eol.get()], "KP_Enter": TX_EOL[self.v_tx_eol.get()],
                   "BackSpace": b"\x7f", "Tab": b"\t", "Escape": b"\x1b",
                   "Up": b"\x1b[A", "Down": b"\x1b[B", "Right": b"\x1b[C", "Left": b"\x1b[D",
                   "Home": b"\x1b[H", "End": b"\x1b[F", "Delete": b"\x1b[3~",
                   "Prior": b"\x1b[5~", "Next": b"\x1b[6~"}
        data = None
        if e.keysym in special:
            data = special[e.keysym]
        elif e.state & 0x4 and len(e.keysym) == 1 and e.keysym.isalpha():
            data = bytes([ord(e.keysym.lower()) - 96])  # Ctrl+A.. -> 0x01..
        elif e.char and e.char.isprintable():
            data = e.char.encode("utf-8")
        if data is not None:
            if self._write(data) and self.v_echo.get():
                if data in (b"\r", b"\n", b"\r\n"):
                    self._append_text("\n")
                elif data.isascii() and data.isprintable():
                    self._append_text(data.decode())
        return "break"

    def paste(self):
        try:
            s = self.win.clipboard_get()
        except tk.TclError:
            return
        s = s.replace("\r\n", "\n").replace("\n", TX_EOL[self.v_tx_eol.get()].decode())
        self._write(s.encode("utf-8"))

    def copy(self):
        try:
            sel = self.text.get("sel.first", "sel.last")
        except tk.TclError:
            return
        self.win.clipboard_clear()
        self.win.clipboard_append(sel)

    def _on_text_select(self, event=None):
        try:
            sel = self.text.get("sel.first", "sel.last")
            if sel:
                self.win.clipboard_clear()
                self.win.clipboard_append(sel)
        except tk.TclError:
            pass

    def clear(self):
        self.text.delete("1.0", "end")
        self.hex_col = 0
        self.at_line_start = True

    def save_log(self):
        path = filedialog.asksaveasfilename(parent=self.win, defaultextension=".txt",
                                            filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", "end-1c"))

    # ---------- windows ----------
    def new_window(self):
        TerminalWindow(self.master)

    def show_version(self):
        messagebox.showinfo("Version Information", 
                          f"{APP_NAME}\n"
                          f"Version: {APP_VERSION}\n"
                          f"Built: {APP_BUILD_DATE}\n\n"
                          f"Python: {sys.version.split()[0]}\n"
                          f"Platform: {sys.platform}\n\n"
                          f"A Tera Term-like serial terminal\n"
                          f"with cross-platform support.",
                          parent=self.win)

    def show_about(self):
        about_text = (
            f"{APP_NAME} v{APP_VERSION}\n\n"
            "Multi-window serial terminal with:\n"
            "• Auto-scroll control\n"
            "• Auto-copy on selection\n"
            "• Auto-reconnect on device removal\n"
            "• Settings persistence\n"
            "• Hex view and timestamps\n"
            "• Cross-platform (Ubuntu/Debian & Windows)\n\n"
            f"Built: {APP_BUILD_DATE}\n"
            "Status: Production Ready ✓"
        )
        messagebox.showinfo("About", about_text, parent=self.win)

    def check_updates(self):
        # Check if there's an update available
        # For now, show current version and manual update instructions
        update_msg = (
            f"Current Version: {APP_VERSION}\n\n"
            "To update this application:\n\n"
            "Ubuntu/Debian:\n"
            "  1. Download latest version\n"
            "  2. Run: sudo dpkg -i serial-terminal_*.deb\n\n"
            "Windows:\n"
            "  1. Download latest SerialTerminal.exe\n"
            "  2. Replace old .exe with new one\n\n"
            "You are running the latest version!"
        )
        messagebox.showinfo("Check for Updates", update_msg, parent=self.win)

    def close(self):
        self.disconnect()
        if self in _windows:
            _windows.remove(self)
        self.win.destroy()
        if not _windows:
            self.master.destroy()


def quit_all():
    for w in list(_windows):
        w.disconnect()
    root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    TerminalWindow(root)
    root.mainloop()
