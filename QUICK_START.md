# Quick Start Guide - Serial Terminal

## 🚀 Fast Setup (Choose Your OS)

### Ubuntu/Debian
```bash
# 1. Make script executable
chmod +x build_deb.sh

# 2. Build DEB package
./build_deb.sh

# 3. Install
sudo dpkg -i dist/serial-terminal_1.0.0_all.deb
sudo apt-get install -f

# 4. Run
serial-terminal
```

**Or run directly from Python:**
```bash
sudo apt-get install python3 python3-tk python3-serial
python3 serial_terminal.py
```

---

### Windows
```cmd
# 1. Install Python 3.8+ from https://www.python.org/downloads/
#    ✅ Check "Add Python to PATH"
#    ✅ Check "tcl/tk and IDLE"

# 2. Right-click build_exe.bat → Run as administrator
#    (Or open Command Prompt and type: build_exe.bat)

# 3. Run
dist\SerialTerminal.exe
```

**Or run directly from Python:**
```cmd
pip install pyserial
python serial_terminal.py
```

---

## ✅ First Use Checklist

- [ ] Install Python (3.6+ for Linux, 3.8+ for Windows)
- [ ] Install tkinter (included with Python)
- [ ] Install pyserial: `pip install pyserial` or `sudo apt-get install python3-serial`
- [ ] Connect USB-to-serial device
- [ ] Launch application
- [ ] Select port from dropdown
- [ ] Click Connect

---

## 📋 Port Selection

### Linux
- `/dev/ttyUSB0` - Common USB-to-serial
- `/dev/ttyACM0` - Arduino, STM32
- `/dev/ttyS0` - Built-in serial port

### Windows
- `COM1`, `COM2`, etc. - Check Device Manager if unsure
- Run Command Prompt as Administrator to access COM ports

---

## ⚙️ Default Settings

| Setting | Value |
|---------|-------|
| Baud Rate | 115200 |
| Data Bits | 8 |
| Parity | None |
| Stop Bits | 1 |
| Flow Control | None |
| Enter Sends | CR |

---

## 🎯 Common Tasks

### Send Data
1. Focus terminal (click on text area)
2. Type your command
3. Press Enter to send

### View in Hex
1. Click Setup menu
2. Check "Hex view"
3. Data now shows in hexadecimal format

### Add Timestamps
1. Click Setup menu
2. Check "Timestamps"
3. Each line shows time like `[13:22:45.123]`

### Save Output
1. Click File menu
2. Click "Save Log..."
3. Choose location and filename

### Control Auto-Scroll
1. Click **"📍 Auto-Scroll: ON"** button in toolbar
2. Toggle between ON (blue) and OFF (gray)

### Copy Data
1. Select text by dragging
2. Data automatically copied to clipboard
3. Paste with Ctrl+V anywhere

---

## ⚠️ Troubleshooting

### No serial ports showing
- Check Device Manager (Windows) or `ls /dev/ttyUSB*` (Linux)
- Verify USB cable is connected
- Install USB-to-serial driver if needed

### "Port is busy"
- Another program has the port open
- Close other terminal applications
- Check running processes

### Can't install DEB package
```bash
sudo apt-get install -f
sudo dpkg -i dist/serial-terminal_1.0.0_all.deb
```

### Python not found (Windows)
- Reinstall Python with "Add Python to PATH" checked
- Restart Command Prompt after installation

### tcl/tk missing (Windows)
- Reinstall Python and select "tcl/tk and IDLE" in installer

---

## 📞 Help

For detailed information, see:
- `README.md` - Full documentation
- `BUILD.md` - Build instructions
- `serial_terminal.py` - Source code

---

**Version**: 1.0.0  
**Last Updated**: October 7, 2026  
**Status**: ✅ Ready to Use
