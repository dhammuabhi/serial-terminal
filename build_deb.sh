#!/bin/bash
# Builds serial-terminal_1.0.0_all.deb from serial_terminal.py

set -e

cd "$(dirname "$0")"

echo ""
echo "============================================"
echo "Serial Terminal - Debian Build Script"
echo "============================================"
echo ""

# Check if required tools are available
if ! command -v dpkg-deb &> /dev/null; then
    echo "ERROR: dpkg-deb is not installed"
    echo "Please install build-essential: sudo apt-get install build-essential"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install: sudo apt-get install python3"
    exit 1
fi

VER=1.0.0
PKG=build/serial-terminal_${VER}_all

echo "Creating package structure..."
rm -rf build
mkdir -p $PKG/DEBIAN $PKG/usr/lib/serial-terminal $PKG/usr/bin \
  $PKG/usr/share/applications $PKG/usr/share/icons/hicolor/scalable/apps

echo "Installing main application..."
install -m 755 serial_terminal.py $PKG/usr/lib/serial-terminal/serial_terminal.py

cat > $PKG/usr/bin/serial-terminal <<'EOS'
#!/bin/sh
exec python3 /usr/lib/serial-terminal/serial_terminal.py "$@"
EOS
chmod 755 $PKG/usr/bin/serial-terminal

echo "Creating application icon..."
cat > $PKG/usr/share/icons/hicolor/scalable/apps/serial-terminal.svg <<'EOS'
<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">
<rect x="8" y="16" width="112" height="96" rx="12" fill="#1e1e1e" stroke="#555" stroke-width="4"/>
<rect x="8" y="16" width="112" height="22" rx="12" fill="#444"/>
<path d="M28 58 l22 16 -22 16" fill="none" stroke="#00e676" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="62" y="88" width="34" height="9" rx="3" fill="#00e676"/>
</svg>
EOS

echo "Creating desktop entry..."
cat > $PKG/usr/share/applications/serial-terminal.desktop <<'EOS'
[Desktop Entry]
Type=Application
Name=Serial Terminal
GenericName=Serial Port Terminal
Comment=Tera Term-like serial communication for /dev/ttyUSB* and /dev/ttyACM*
Exec=serial-terminal
Icon=serial-terminal
Terminal=false
Categories=Utility;Development;System;
Keywords=serial;com;port;uart;terminal;teraterm;ttyUSB;
StartupWMClass=Tk
EOS

echo "Creating package metadata..."
cat > $PKG/DEBIAN/control <<EOS
Package: serial-terminal
Version: $VER
Section: utils
Priority: optional
Architecture: all
Depends: python3, python3-tk, python3-serial
Maintainer: $USER <$USER@localhost>
Description: Tera Term-like serial terminal
 Multi-window serial terminal for /dev/ttyUSB* and /dev/ttyACM* ports
 with baud rate, parity, stop bits and flow control settings.
EOS

echo "Creating post-install scripts..."
cat > $PKG/DEBIAN/postinst <<'EOS'
#!/bin/sh
set -e
command -v update-desktop-database >/dev/null && update-desktop-database -q /usr/share/applications || true
command -v gtk-update-icon-cache >/dev/null && gtk-update-icon-cache -q -t /usr/share/icons/hicolor || true
EOS
chmod 755 $PKG/DEBIAN/postinst
cp $PKG/DEBIAN/postinst $PKG/DEBIAN/postrm

chmod -R g-w,o-w $PKG

echo "Building DEB package..."
dpkg-deb --root-owner-group --build $PKG dist_tmp.deb >/dev/null

mkdir -p dist
mv dist_tmp.deb dist/serial-terminal_${VER}_all.deb
rm -rf build

echo ""
echo "============================================"
echo "✓ Successfully built DEB package"
echo "============================================"
echo ""
echo "Location: dist/serial-terminal_${VER}_all.deb"
echo ""
echo "To install:"
echo "  sudo dpkg -i dist/serial-terminal_${VER}_all.deb"
echo "  sudo apt-get install -f  # Fix missing dependencies if needed"
echo ""
echo "To run:"
echo "  serial-terminal"
echo ""
echo "To uninstall:"
echo "  sudo apt-get remove serial-terminal"
echo ""
