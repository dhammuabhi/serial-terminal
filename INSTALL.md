# Installation Guide - Serial Terminal

Complete step-by-step installation for all platforms.

---

## Ubuntu/Debian Installation

### Option 1: Using Pre-built DEB Package (Recommended)

#### Prerequisites
- Ubuntu 18.04+ or Debian 10+
- `sudo` access

#### Steps

1. **Build the package** (or use pre-built)
   ```bash
   cd ~/ComPortApp
   chmod +x build_deb.sh
   ./build_deb.sh
   ```

2. **Install the package**
   ```bash
   sudo dpkg -i dist/serial-terminal_1.0.0_all.deb
   sudo apt-get install -f  # Install missing dependencies
   ```

3. **Run the application**
   ```bash
   serial-terminal
   ```

4. **Verify installation**
   ```bash
   which serial-terminal
   serial-terminal --version  # If available
   ```

#### Uninstall
```bash
sudo apt-get remove serial-terminal
```

---

### Option 2: Install from Source

#### Prerequisites
```bash
sudo apt-get install python3 python3-tk python3-dev
```

#### Install pyserial
```bash
# Method 1: Using apt
sudo apt-get install python3-serial

# Method 2: Using pip
pip3 install pyserial
```

#### Run
```bash
cd ~/ComPortApp
python3 serial_terminal.py
```

#### Fix permissions for USB/serial access
```bash
# Add current user to dialout group
sudo usermod -a -G dialout $USER

# Apply group changes (log out and log back in)
newgrp dialout

# Or restart your computer
sudo reboot
```

---

### Troubleshooting Ubuntu/Debian

**Problem: "Python3 command not found"**
```bash
sudo apt-get update
sudo apt-get install python3
```

**Problem: "No module named 'tkinter'"**
```bash
sudo apt-get install python3-tk
```

**Problem: "No module named 'serial'"**
```bash
# Method 1
sudo apt-get install python3-serial

# Method 2
pip3 install pyserial
```

**Problem: "Permission denied" accessing serial port**
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER
# Log out and log back in
```

**Problem: "dpkg: error" during installation**
```bash
sudo apt-get install -f
sudo dpkg -i dist/serial-terminal_1.0.0_all.deb
```

**Problem: Build script won't run**
```bash
chmod +x build_deb.sh
./build_deb.sh
```

---

## Windows Installation

### Option 1: Using Pre-built EXE (Recommended)

#### Prerequisites
- Windows 7+
- Administrator access (optional, for COM port access)

#### Steps

1. **Install Python 3.8+** from [python.org](https://www.python.org/downloads/)
   - Download: "Windows installer (64-bit)" or "(32-bit)"
   - ✅ **IMPORTANT**: Check "Add Python to PATH" during installation
   - ✅ **IMPORTANT**: Check "tcl/tk and IDLE" during installation
   - Click "Install Now" or customize

2. **Build the executable** (requires Build Tools)
   ```cmd
   # Open Command Prompt as Administrator
   cd C:\Path\To\ComPortApp
   build_exe.bat
   ```
   
   OR build manually:
   ```cmd
   pip install pyinstaller pyserial
   pyinstaller --onefile --windowed --name SerialTerminal serial_terminal.py
   ```

3. **Run the application**
   - Double-click `dist\SerialTerminal.exe`
   - Or from Command Prompt: `dist\SerialTerminal.exe`

4. **Create Desktop Shortcut** (Optional)
   - Right-click `dist\SerialTerminal.exe`
   - Select "Send to" → "Desktop (create shortcut)"

#### Uninstall
- Delete `dist\SerialTerminal.exe` folder
- Delete any shortcuts

---

### Option 2: Run from Python

#### Prerequisites
- Python 3.8+ installed from [python.org](https://www.python.org/downloads/)

#### Install dependencies
```cmd
pip install pyserial
```

#### Run
```cmd
cd C:\Path\To\ComPortApp
python serial_terminal.py
```

---

### Option 3: Portable Build (Advanced)

Create a completely portable version:

```cmd
pip install pyinstaller
pyinstaller --onefile --windowed ^
    --add-data "C:\Python310\tcltk:tcltk" ^
    --name SerialTerminal serial_terminal.py
```

---

### Windows Troubleshooting

**Problem: "Python is not recognized as an internal or external command"**
- Reinstall Python with "Add Python to PATH" checked
- Or add Python to PATH manually:
  1. Open Environment Variables (search in Start menu)
  2. Add Python installation path (e.g., `C:\Users\YourName\AppData\Local\Programs\Python\Python310`)

**Problem: "ModuleNotFoundError: No module named 'pyinstaller'"**
```cmd
pip install pyinstaller
```

**Problem: "ModuleNotFoundError: No module named 'serial'"**
```cmd
pip install pyserial
```

**Problem: "tcl/tk was not installed"**
- Reinstall Python
- In installer, make sure to check "tcl/tk and IDLE"
- Can also install via: `pip install tk`

**Problem: "Build script won't run as batch file"**
- Open Command Prompt as Administrator
- Navigate to the folder: `cd /d "C:\Path\To\ComPortApp"`
- Run: `build_exe.bat`

**Problem: "Access is denied" for COM port**
- Run as Administrator
- Right-click `SerialTerminal.exe` → "Run as administrator"
- Or right-click application shortcut → Advanced → "Run as administrator"

**Problem: Serial port not showing up**
- Check Device Manager:
  - Right-click "Start" button → "Device Manager"
  - Look under "Ports (COM & LPT)"
  - If showing as "Unknown Device" or with error, install USB-to-Serial drivers

**Problem: "The name of the Python installation path is not found"**
- Make sure Python is installed
- Check that PATH is correctly set
- Restart Command Prompt after setting PATH

---

## macOS Installation (Experimental)

### Prerequisites
- Python 3.8+ from [python.org](https://www.python.org/downloads/)
- Or via Homebrew: `brew install python3 tk`

### Install Dependencies
```bash
pip3 install pyserial
```

### Run
```bash
python3 serial_terminal.py
```

### Build Executable
```bash
pip3 install pyinstaller
pyinstaller --onefile --windowed --name SerialTerminal serial_terminal.py
# Output: dist/SerialTerminal.app
```

---

## Verification After Installation

### Ubuntu/Debian
```bash
# Check installation
which serial-terminal
dpkg -l | grep serial-terminal

# Test run
serial-terminal

# Check version
file /usr/bin/serial-terminal
```

### Windows
```cmd
# Check Python installation
python --version
pip list | find "pyserial"

# Test run
dist\SerialTerminal.exe
```

---

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **OS** | Ubuntu 18.04 / Windows 7 | Ubuntu 20.04+ / Windows 10+ |
| **Python** | 3.6 (Linux) / 3.8 (Windows) | 3.9+ |
| **RAM** | 256 MB | 512 MB+ |
| **Disk** | 50 MB | 100 MB |
| **tkinter** | Required | Included with Python |
| **pyserial** | Required | 3.5+ |

---

## Getting Help

1. **Check the troubleshooting section above**
2. **Read README.md for features and usage**
3. **Read QUICK_START.md for quick reference**
4. **Check BUILD.md for build instructions**

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Port not visible | Check Device Manager (Windows) or `ls /dev/ttyUSB*` (Linux) |
| "Port is busy" | Close other terminal applications |
| Can't access port | Run as Administrator (Windows) or check permissions (Linux) |
| Module not found | Run `pip install pyserial` |
| Build fails | Ensure Python is in PATH and build tools installed |

---

## Reinstall/Repair

### Ubuntu/Debian
```bash
# Uninstall
sudo apt-get remove serial-terminal

# Clean build files
rm -rf build dist

# Rebuild
chmod +x build_deb.sh
./build_deb.sh

# Reinstall
sudo dpkg -i dist/serial-terminal_1.0.0_all.deb
sudo apt-get install -f
```

### Windows
```cmd
# Delete old build
rmdir /s dist build

# Clean Python cache
python -m pip cache purge

# Rebuild
build_exe.bat
```

---

**Version**: 1.0.0  
**Last Updated**: October 7, 2026  
**Status**: ✅ Ready to Install
