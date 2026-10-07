# Serial Terminal Build Guide

## Overview
Serial Terminal is a Tera Term-like serial communication application for Linux and Windows.

### Features
- Multi-window support
- Configurable baud rate, parity, stop bits, flow control
- Hex view and timestamp modes
- Local echo and auto-scroll options
- Auto-reconnect on device removal
- Cross-platform (Ubuntu/Debian and Windows)

---

## Building on Ubuntu/Debian

### Prerequisites
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-tk python3-dev dpkg-dev build-essential
```

### Build DEB Package
```bash
chmod +x build_deb.sh
./build_deb.sh
```

This creates: `dist/serial-terminal_1.0.0_all.deb`

### Install DEB Package
```bash
sudo dpkg -i dist/serial-terminal_1.0.0_all.deb
sudo apt-get install -f  # Fix any missing dependencies
```

### Run from Command Line
```bash
serial-terminal
```

### Uninstall
```bash
sudo apt-get remove serial-terminal
```

---

## Building on Windows

### Prerequisites
1. Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
   - ✅ **Important**: Check "Add Python to PATH" during installation
   - ✅ **Important**: Check "tcl/tk and IDLE" during installation

2. Install required tools (Run Command Prompt as Administrator):
```cmd
pip install --upgrade pip
pip install pyserial pyinstaller
```

### Build EXE
Double-click `build_exe.bat` or run from Command Prompt:
```cmd
build_exe.bat
```

This creates: `dist\SerialTerminal.exe`

### Run the Application
- Double-click `dist\SerialTerminal.exe`
- Or from Command Prompt: `dist\SerialTerminal.exe`

### Create Windows Shortcut (Optional)
1. Right-click `dist\SerialTerminal.exe`
2. Select "Send to" → "Desktop (create shortcut)"
3. Optionally rename the shortcut

### Uninstall
Simply delete `dist\SerialTerminal.exe` and the folder

---

## Troubleshooting

### Ubuntu/Debian Issues

**"python3: command not found"**
```bash
sudo apt-get install python3
```

**"ModuleNotFoundError: No module named 'tkinter'"**
```bash
sudo apt-get install python3-tk
```

**"dpkg: error while setting up (--install)"**
```bash
sudo apt-get install -f
sudo dpkg -i dist/serial-terminal_1.0.0_all.deb
```

**Permission denied when running build script**
```bash
chmod +x build_deb.sh
./build_deb.sh
```

### Windows Issues

**"Python is not recognized as an internal or external command"**
- Reinstall Python from python.org with "Add Python to PATH" checked
- Or add Python to PATH manually in Environment Variables

**"ModuleNotFoundError: No module named 'pyinstaller'"**
```cmd
pip install pyinstaller
```

**"tcl/tk was not installed"**
- Reinstall Python and ensure "tcl/tk and IDLE" is selected in the installation dialog

**"PyInstaller command not found"**
```cmd
python -m pip install pyinstaller
python -m PyInstaller --onefile --windowed serial_terminal.py
```

---

## Manual Build without Build Scripts

### Ubuntu/Debian - Create DEB Manually
```bash
mkdir -p build/serial-terminal_1.0.0_all/{DEBIAN,usr/lib/serial-terminal,usr/bin}
cp serial_terminal.py build/serial-terminal_1.0.0_all/usr/lib/serial-terminal/
# ... (add DEBIAN/control and other files)
dpkg-deb --build build/serial-terminal_1.0.0_all dist/serial-terminal_1.0.0_all.deb
```

### Windows - Create EXE Manually
```cmd
pip install pyinstaller pyserial
pyinstaller --onefile --windowed --name SerialTerminal serial_terminal.py
# Output in dist\SerialTerminal.exe
```

---

## Developer Notes

### Dependencies
- **Python 3.6+** (Ubuntu/Debian) or **Python 3.8+** (Windows)
- **tkinter** (included with Python)
- **pyserial** (external, installed via pip/apt)

### File Structure
```
ComPortApp/
├── serial_terminal.py      # Main application
├── requirements.txt        # Python dependencies
├── build_deb.sh           # Ubuntu/Debian build script
├── build_exe.bat          # Windows build script
├── BUILD.md               # This file
├── dist/                  # Built packages (created after build)
└── .codex                 # Codex configuration
```

### Key Features in Code
- Multi-window management with shared port tracking
- Graceful device removal handling with auto-reconnect
- Settings persistence in `~/.config/serial-terminal/settings.json`
- Cross-platform compatibility (Linux/Windows)

---

## Support

For issues or feature requests, ensure you have:
1. ✅ Latest Python version installed
2. ✅ All dependencies installed (`pip install -r requirements.txt`)
3. ✅ Proper permissions (use `chmod +x` for Linux scripts)
4. ✅ Run as Administrator on Windows for COM port access

---

**Last Updated**: October 7, 2026
**Version**: 1.0.0
