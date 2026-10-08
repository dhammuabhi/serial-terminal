# 🔌 Serial Terminal - Multi-Window Serial Port Communication

A **Tera Term-like serial terminal** for Linux and Windows with cross-platform support, auto-scroll, auto-reconnect, and keyboard-driven workflow.

[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-brightgreen)](https://github.com/dhammuabhi/serial-terminal)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success)]()

---

## ✨ Key Features

### 🔌 Core Functionality
- ✅ **Multi-window support** - Open multiple serial terminals simultaneously
- ✅ **Real-time serial communication** - Send and receive data instantly
- ✅ **Automatic port detection** - Automatically lists available COM/serial ports
- ✅ **Fast port switching** - Switch between ports without losing data
- ✅ **Configurable settings** - Baud rate, data bits, parity, stop bits, flow control
- ✅ **Persistent settings** - Automatically saves your preferences for next session

### ⌨️ Keyboard-Driven Workflow

#### Main Shortcuts
| Shortcut | Action | Description |
|----------|--------|-------------|
| **Alt + I** | Disconnect | Disconnect from current COM port |
| **Alt + N** | New Connection | Open interactive port selector |
| **Alt + D** | Duplicate Session | Create new window with same settings |
| **Alt + Q** | Exit | Close current window |
| **Alt + F4** | Exit | Alternative exit shortcut |
| **Alt + Z** | Auto-Scroll | Toggle auto-scroll ON/OFF |
| **Alt + M** | Maximize | Toggle full-screen mode |
| **Ctrl + N** | New Window | Open new terminal window |
| **Ctrl + W** | Close | Close current window |
| **Ctrl+Shift+C** | Copy | Copy selected text |
| **Ctrl+Shift+V** | Paste | Paste from clipboard (sends to port) |

### 🎯 Interactive Port Selector (Alt+N)

When you press **Alt+N**, an interactive dialog opens:

```
┌──────────────────────────────┐
│   Select COM Port            │
├──────────────────────────────┤
│ Available COM Ports:         │
│                              │
│ ┌────────────────────────┐   │
│ │ /dev/ttyUSB0 ←CURRENT  │   │
│ │ /dev/ttyUSB1           │   │
│ │ /dev/ttyACM0           │   │
│ └────────────────────────┘   │
│                              │
│ ↑↓ Navigate | Enter Connect  │
│ Esc Cancel                   │
│                              │
│  [Connect]  [Cancel]        │
└──────────────────────────────┘
```

**Features:**
- **Pre-selected** - Your current port is highlighted
- **Keyboard navigation** - Use ↑↓ arrows to navigate
- **Quick connect** - Press Enter to connect
- **Easy cancel** - Press Escape to cancel
- **Double-click** - Quick select and connect
- **Smart switching** - Automatically disconnects old port before connecting new

### 🖥️ Terminal Features
- ✅ **Black terminal theme** - Easy on the eyes with light text on dark background
- ✅ **Auto-scroll** - Automatically scroll to bottom as data arrives
- ✅ **Auto-scroll toggle** - Quick button and Alt+Z shortcut
- ✅ **Auto-copy on selection** - Automatically copy selected text to clipboard
- ✅ **Hex view mode** - Display incoming data in hexadecimal format
- ✅ **Timestamp display** - Add timestamps to incoming data
- ✅ **Local echo** - Echo sent data back to screen
- ✅ **Clear screen** - Quick clear command
- ✅ **Large scrollback** - 20,000 lines of history
- ✅ **Backspace support** - Full backspace handling for terminal emulation

### 🔄 Auto-Reconnect
- ✅ **Device removal detection** - Automatically detects when device is disconnected
- ✅ **Auto-reconnect** - Attempts to reconnect when device reappears
- ✅ **Manual reconnect** - Or use Alt+N to manually select and connect
- ✅ **Status indication** - Shows connection status in window title and status bar

### 💾 Data Management
- ✅ **Save log file** - Export terminal output to text file
- ✅ **Full scrollback** - Access all 20,000 lines of history
- ✅ **Clear screen** - Clear terminal without losing connection
- ✅ **DTR/RTS control** - Full control over serial signal lines

### 🌍 Cross-Platform
- ✅ **Linux support** - Ubuntu, Debian, Fedora, and other distributions
- ✅ **Windows support** - Windows 10, Windows 11
- ✅ **Consistent UI** - Same look and feel across platforms
- ✅ **Platform-specific packaging** - DEB for Linux, EXE for Windows

---

## 🚀 Quick Start

### Installation

#### 🐧 Ubuntu/Debian Linux

##### Option 1: Using DEB Package (Recommended)

**First-time installation:**
```bash
# Download the latest DEB package
cd /tmp
wget https://github.com/dhammuabhi/serial-terminal/releases/download/v1.1.0/serial-terminal_1.1.0_all.deb

# Install the package
sudo dpkg -i serial-terminal_1.1.0_all.deb

# If dependencies are missing, fix them
sudo apt-get install -f

# Launch the application
serial-terminal
```

**Updating to newer version:**
```bash
# Download the new version
cd /tmp
wget https://github.com/dhammuabhi/serial-terminal/releases/download/v1.1.0/serial-terminal_1.1.0_all.deb

# The new version will automatically replace the old one
sudo dpkg -i serial-terminal_1.1.0_all.deb

# Verify the update
serial-terminal --version
```

**Uninstalling:**
```bash
# Remove the application
sudo apt-get remove serial-terminal

# Or using dpkg
sudo dpkg -r serial-terminal
```

##### Option 2: Using Standalone Executable

**First-time installation:**
```bash
# Download the executable
cd /tmp
wget https://github.com/dhammuabhi/serial-terminal/releases/download/v1.1.0/SerialTerminal-Linux

# Make it executable
chmod +x SerialTerminal-Linux

# Run directly
./SerialTerminal-Linux

# Optional: Move to a system path for easy access
sudo mv SerialTerminal-Linux /usr/local/bin/serial-terminal
sudo chmod +x /usr/local/bin/serial-terminal

# Now you can run from anywhere
serial-terminal
```

**Updating to newer version:**
```bash
# Simply download and replace the executable
cd /tmp
wget https://github.com/dhammuabhi/serial-terminal/releases/download/v1.1.0/SerialTerminal-Linux
chmod +x SerialTerminal-Linux

# Replace the old one
sudo mv SerialTerminal-Linux /usr/local/bin/serial-terminal

# Run the new version
serial-terminal
```

**Uninstalling:**
```bash
# If using system path
sudo rm /usr/local/bin/serial-terminal

# Or simply delete the executable file
```

---

#### 🪟 Windows

##### Option 1: Using Standalone Executable (Recommended)

**First-time installation:**
```
1. Visit: https://github.com/dhammuabhi/serial-terminal/releases
2. Download: SerialTerminal.exe (latest version)
3. Double-click SerialTerminal.exe to run
4. Optional: Create a shortcut on Desktop
   - Right-click SerialTerminal.exe
   - Select "Send to" → "Desktop (create shortcut)"
```

**Updating to newer version:**
```
1. Visit: https://github.com/dhammuabhi/serial-terminal/releases
2. Download: Latest SerialTerminal.exe
3. Replace the old SerialTerminal.exe with new one
4. Or keep multiple versions with different names:
   - SerialTerminal-v1.0.0.exe
   - SerialTerminal-v1.1.0.exe
```

**Uninstalling:**
```
1. Simply delete SerialTerminal.exe
2. Settings will be preserved in: C:\Users\YourUsername\AppData\Roaming\serial-terminal\
3. Delete the folder above if you want to remove settings too
```

##### Option 2: Using Command Line

**First-time installation:**
```powershell
# Open PowerShell as Administrator
# Download using curl
curl -L https://github.com/dhammuabhi/serial-terminal/releases/download/v1.1.0/SerialTerminal.exe -o C:\Users\%USERNAME%\Desktop\SerialTerminal.exe

# Run the application
C:\Users\%USERNAME%\Desktop\SerialTerminal.exe
```

**Updating to newer version:**
```powershell
# Download the new version (will overwrite old one)
curl -L https://github.com/dhammuabhi/serial-terminal/releases/download/v1.1.0/SerialTerminal.exe -o C:\Users\%USERNAME%\Desktop\SerialTerminal.exe
```

---

#### From Source Code (Any Platform)

**First-time installation:**
```bash
# Clone the repository
git clone https://github.com/dhammuabhi/serial-terminal.git
cd serial-terminal

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 serial_terminal.py
```

**Updating to newer version:**
```bash
# Navigate to the project directory
cd serial-terminal

# Pull the latest changes
git pull origin main

# Run the updated version
python3 serial_terminal.py
```

**Uninstalling:**
```bash
# Simply delete the directory
rm -rf serial-terminal
```

---

### Version Checking

**Check installed version:**
```bash
# Ubuntu/Debian (using DEB)
apt-cache policy serial-terminal

# Linux (using executable)
serial-terminal --version

# Windows (using executable)
SerialTerminal.exe --version

# From source
python3 serial_terminal.py --version
```

---

### Basic Usage

1. **Launch the application**
   - **Ubuntu/Debian**: `serial-terminal`
   - **Windows**: Double-click `SerialTerminal.exe`
   - **From source**: `python3 serial_terminal.py`

2. **Connect to a port**
   - Click "Connect" button in toolbar, OR
   - Press **Alt+N** to open interactive port selector
   - Select a port and press Enter

3. **Send data**
   - Type in the terminal
   - Press Enter to send (line ending configurable)

4. **Receive data**
   - Data automatically appears in terminal
   - Auto-scroll keeps latest data visible

5. **Switch ports**
   - Press **Alt+N** anytime
   - Select different port
   - Press Enter (old port disconnects, new port connects)

6. **Disconnect**
   - Click "Disconnect" button, OR
   - Press **Alt+I**



## 🎛️ Configuration

### Serial Port Settings

Access via **Setup → Serial port...** or double-click **Settings** button:

- **Data bits** - 5, 6, 7, or 8 bits
- **Parity** - None, Even, Odd, Mark, Space
- **Stop bits** - 1, 1.5, or 2 bits
- **Flow control** - None, RTS/CTS, XON/XOFF, DSR/DTR
- **Enter sends** - CR, LF, or CR+LF
- **Local echo** - Echo typed characters
- **Hex view** - Display data as hex
- **Timestamps** - Add timestamps to data
- **Auto-scroll** - Auto-scroll to new data
- **DTR/RTS** - Manual signal control

**Note:** Port settings cannot be changed while connected. Disconnect first, then adjust settings.

### Settings Persistence

Your settings are automatically saved in:
- **Linux/Mac**: `~/.config/serial-terminal/settings.json`
- **Windows**: `%APPDATA%\serial-terminal\settings.json`

Settings are loaded automatically on next launch.

---

## 📋 Menu Reference

### File Menu
- **New Window** (Ctrl+N) - Open additional terminal window
- **New Connection** (Alt+N) - Interactive port selector
- **Duplicate Session** (Alt+D) - Copy current window with all settings
- **Save Log...** - Export terminal output to file
- **Disconnect** (Alt+I) - Disconnect from current port
- **Close Window** (Ctrl+W) - Close current window
- **Exit (close all)** (Alt+Q) - Close all windows and exit

### Edit Menu
- **Copy** (Ctrl+Shift+C) - Copy selected text
- **Paste (send)** (Ctrl+Shift+V) - Send clipboard to serial port
- **Clear Screen** - Clear terminal (connection remains active)

### Setup Menu
- **Serial port...** - Configure port settings
- **Local echo** - Toggle echo of sent characters
- **Hex view** - Toggle hexadecimal display mode
- **Timestamps** - Toggle timestamp display
- **Auto-scroll** (Alt+Z) - Toggle auto-scroll feature
- **DTR** - Toggle DTR signal line
- **RTS** - Toggle RTS signal line
- **Send Break** - Send break signal
- **Maximize/Minimize** (Alt+M) - Toggle full-screen mode

### Help Menu
- **About** - Application information
- **Check for Updates** - Check version info
- **View Version** - Detailed version information

---

## 🎮 Advanced Usage

### Multi-Window Workflow

Open multiple terminals to monitor different devices:

```bash
# Window 1: Connected to /dev/ttyUSB0
Alt+D  # Duplicate session
# Window 2: Same settings, disconnected

Alt+N  # Open port selector
# Select /dev/ttyUSB1
# Now has two windows monitoring different ports
```

### Data Logging and Analysis

```bash
# While connected, receive data
# File → Save Log → choose filename
# Data exported to text file for analysis
```

### Hex Mode for Binary Data

```bash
Setup → Hex view  # Toggle on
# Data now displays in hexadecimal format
# Useful for binary protocols and debugging
```

### Automated Port Switching

When monitoring multiple devices:

1. Connect to Port A
2. Press Alt+N
3. Navigate to Port B
4. Press Enter
5. Instantly switched to Port B (A automatically disconnected)

No manual disconnect needed!

---

## 🔧 Troubleshooting

### Port Not Appearing
- Check device connections
- Install USB-to-serial drivers if needed
- On Linux, try: `ls /dev/ttyUSB*` or `ls /dev/ttyACM*`
- Check device permissions: `ls -l /dev/ttyUSB0`

### Permission Denied Error
```bash
# Linux: Add user to dialout group
sudo usermod -aG dialout $USER
# Then log out and log back in
```

### Port Shows "Busy"
- Another application has the port open
- Check running processes: `lsof /dev/ttyUSB0`
- Close the other application or port

### Connection Lost / Device Removed
- Terminal shows "[Connection lost (device removed?)]"
- Plug device back in
- Press Alt+N to reconnect
- Or wait for auto-reconnect

### Data Not Sending
- Verify connection: Check window title shows port name
- Check baud rate matches device
- Check flow control settings
- Try with local echo enabled to see what's being sent

---

## 📦 Requirements

### System Requirements
- **CPU**: 1 GHz or faster
- **RAM**: 128 MB minimum
- **Storage**: 50 MB
- **Display**: 800x600 minimum

### Software Requirements
- **Python**: 3.7 or later
- **Tkinter**: Usually included with Python
- **pyserial**: Installed via requirements.txt

### Platform Support
| Platform | Status | Notes |
|----------|--------|-------|
| Ubuntu 18.04+ | ✅ Fully supported | Tested and verified |
| Debian 10+ | ✅ Fully supported | DEB package available |
| Fedora | ✅ Works | Install from source |
| Windows 10+ | ✅ Fully supported | EXE available |
| macOS | ⚠️ Untested | Should work from source |

---

## 🔌 Serial Port Configuration Examples

### Arduino (Default)
```
Baud: 9600
Data bits: 8
Parity: None
Stop bits: 1
Flow control: None
```

### FTDI Devices
```
Baud: 115200
Data bits: 8
Parity: None
Stop bits: 1
Flow control: None
```

### Industrial Equipment
```
Baud: 19200
Data bits: 8
Parity: Even
Stop bits: 1
Flow control: RTS/CTS (often required)
```

---

## 🤝 Contributing

Found a bug or have a feature request? 

1. Open an issue on GitHub
2. Describe the problem with steps to reproduce
3. Include your OS and Python version
4. Attach screenshots if applicable

---

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## 👨‍💻 Author

**Abhilash Dhammu**
- GitHub: [@dhammuabhi](https://github.com/dhammuabhi)
- Project: [Serial Terminal](https://github.com/dhammuabhi/serial-terminal)

---

## 📚 Additional Resources

- **INSTALL.md** - Detailed installation guide
- **BUILD.md** - Build system documentation
- **QUICK_START.md** - Quick reference card
- **PROJECT_SUMMARY.md** - Project structure and components

---

## 🎯 Version History

### v1.0.0 (October 2026) - Initial Release
- ✅ Multi-window terminal support
- ✅ All keyboard shortcuts (Alt+I, N, Q, D, Z, M)
- ✅ Interactive port selector with keyboard navigation
- ✅ Auto-disconnect/reconnect on port switching
- ✅ Auto-scroll and auto-reconnect features
- ✅ Settings persistence
- ✅ Cross-platform support (Linux & Windows)
- ✅ Full Tera Term-like emulation

---

## 🚀 Getting Help

### Common Issues

**Q: How do I know which port my device is on?**
- Look in the port dropdown - it shows all available ports
- Or use Alt+N to see the interactive selector
- On Linux: `ls /dev/tty*`
- On Windows: Device Manager → Ports

**Q: Can I use multiple terminals at once?**
- Yes! Press Ctrl+N or Alt+D to open more windows
- Each can connect to different ports
- Perfect for monitoring multiple devices

**Q: How do I automate terminal commands?**
- Use Alt+N for keyboard-driven port selection
- Settings persist, so configure once, run always
- Save logs for data analysis

**Q: What if my device isn't showing up?**
- Install USB drivers if needed
- Check USB cable connection
- Try a different USB port
- Restart the application

---

## 📊 Feature Comparison

| Feature | Serial Terminal | Tera Term | PuTTY | minicom |
|---------|-----------------|-----------|-------|---------|
| Multi-window | ✅ | ⚠️ Limited | ✅ | ❌ |
| Linux | ✅ | ❌ | ✅ | ✅ |
| Windows | ✅ | ✅ | ✅ | ❌ |
| Auto-scroll | ✅ | ⚠️ Manual | ⚠️ Manual | ❌ |
| Auto-reconnect | ✅ | ❌ | ❌ | ❌ |
| Keyboard shortcuts | ✅ | ✅ | ⚠️ Limited | ⚠️ Limited |
| Settings persistence | ✅ | ✅ | ✅ | ✅ |
| Simple UI | ✅ | ✅ | ⚠️ Complex | ✅ |

---

## 💡 Tips and Tricks

### Tip 1: Quick Port Switching
Instead of menus, just press **Alt+N**, navigate with arrows, press **Enter**. Takes 2 seconds!

### Tip 2: Clone Terminal Window
Need to monitor another device? Press **Alt+D** to duplicate current window with all settings.

### Tip 3: Save Important Data
Before disconnecting, use **File → Save Log** to export terminal output.

### Tip 4: Full-Screen Mode
Working with lots of data? Press **Alt+M** to maximize the terminal window.

### Tip 5: Auto-Scroll Toggle
Quick toggle with **Alt+Z** or the button in toolbar.

---

## 🐛 Known Limitations

- Tkinter may have issues with very high baud rates (>2M baud)
- Terminal emulation is basic (no ANSI color codes)
- Limited to 20,000 lines of scrollback history
- No recording/playback feature (use Save Log instead)

---

## 🔐 Security Note

This application does not modify, upload, or send your data anywhere. All communication is local to your computer. Open source - you can verify the code yourself!

---

## 📞 Support

- **Issues & Bugs**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Feature Requests**: GitHub Issues (with `[FEATURE]` tag)

---

**Enjoy using Serial Terminal!** 🎉

For the latest version and updates, visit:
https://github.com/dhammuabhi/serial-terminal
