# Version Management Guide

## Overview

Serial Terminal now includes built-in version management with the ability to display and update version information throughout the application.

---

## Version Information

### Current Version
- **Version**: 1.0.0
- **Release Date**: October 7, 2026
- **Status**: Production Ready ✓

### Version Constants (in `serial_terminal.py`)

```python
APP_NAME = "Serial Terminal"
APP_VERSION = "1.0.0"
APP_BUILD_DATE = "October 7, 2026"
```

**Location in file**: Lines 17-19

---

## Where Version is Displayed

### 1. Window Title (Always Visible)
```
When Disconnected:
  "Serial Terminal v1.0.0 - disconnected"

When Connected:
  "Serial Terminal v1.0.0 - COM5"
```

### 2. Help Menu Options

| Menu Item | Information Shown |
|-----------|------------------|
| **About** | App name, version, features, build date |
| **View Version** | Version, Python version, platform, build date |
| **Check for Updates** | Current version, update instructions |

---

## How to Update Version

### Step 1: Edit Version Constants

Open `serial_terminal.py` and find these lines (around line 17):

```python
APP_NAME = "Serial Terminal"
APP_VERSION = "1.0.0"           # ← Update this
APP_BUILD_DATE = "October 7, 2026"  # ← Update this
```

Change to new version:
```python
APP_NAME = "Serial Terminal"
APP_VERSION = "1.0.1"           # New version
APP_BUILD_DATE = "October 10, 2026"  # New date
```

### Step 2: Rebuild Packages

**For Ubuntu/Debian:**
```bash
chmod +x build_deb.sh
./build_deb.sh
```

Creates: `dist/serial-terminal_1.0.0_all.deb`

**For Windows:**
```cmd
build_exe.bat
```

Creates: `dist\SerialTerminal.exe`

### Step 3: Test New Version

1. Install/run the new package
2. Check window title shows new version
3. Open Help → View Version to verify
4. Check Help → About for correct information

---

## Version Numbering Scheme

We use **Semantic Versioning**: `MAJOR.MINOR.PATCH`

### Examples:
- `1.0.0` - Initial release
- `1.0.1` - Bug fix (patch)
- `1.1.0` - New feature (minor)
- `2.0.0` - Breaking change (major)

### When to increment:
- **MAJOR** (x.0.0): Incompatible changes
- **MINOR** (1.x.0): New features, backward compatible
- **PATCH** (1.0.x): Bug fixes only

---

## Version History Template

Keep track of changes in this format:

```markdown
## Version 1.0.1 (October 10, 2026)
- Bug fix: Fixed auto-reconnect timeout
- Feature: Added keyboard shortcut help
- Improvement: Better error messages

## Version 1.0.0 (October 7, 2026)
- Initial release
- Multi-window support
- Auto-scroll, auto-copy, auto-reconnect
- Settings persistence
```

---

## Implementation Details

### Help Menu Items

#### About Dialog
```python
def show_about(self):
    # Shows:
    # - App name and version
    # - Key features list
    # - Build date
    # - Status
```

**Triggered by**: Help → About

#### Version Info Dialog
```python
def show_version(self):
    # Shows:
    # - Version number
    # - Python version
    # - Platform (Windows/Linux/macOS)
    # - Build date
```

**Triggered by**: Help → View Version

#### Update Check Dialog
```python
def check_updates(self):
    # Shows:
    # - Current version
    # - Ubuntu/Debian update instructions
    # - Windows update instructions
    # - Encouragement message
```

**Triggered by**: Help → Check for Updates

---

## Version Display Locations

### Automatic (No Code Changes Needed)

| Location | Display Format |
|----------|-----------------|
| Window Title | "Serial Terminal v1.0.0 - [status]" |
| About Dialog | "Serial Terminal v1.0.0" |
| Version Dialog | "Version: 1.0.0" |
| Update Dialog | "Current Version: 1.0.0" |

Once you update `APP_VERSION`, it automatically appears everywhere.

---

## Release Checklist

When releasing a new version:

- [ ] Update `APP_VERSION` in code
- [ ] Update `APP_BUILD_DATE` in code
- [ ] Test application starts without errors
- [ ] Verify window title shows new version
- [ ] Check Help → About shows correct info
- [ ] Check Help → View Version shows correct info
- [ ] Rebuild DEB package (Ubuntu/Debian)
- [ ] Rebuild EXE file (Windows)
- [ ] Test both builds
- [ ] Update documentation/README if needed
- [ ] Commit changes to version control
- [ ] Tag release with version number
- [ ] Create release notes

---

## Command Reference

### View Current Version (Programmatically)
```python
print(APP_VERSION)  # Output: 1.0.0
print(APP_BUILD_DATE)  # Output: October 7, 2026
```

### Update Version (Quick Commands)
```bash
# On Linux/macOS - Replace version in code
sed -i 's/APP_VERSION = "1.0.0"/APP_VERSION = "1.0.1"/g' serial_terminal.py

# Then rebuild
./build_deb.sh
```

```cmd
# On Windows - Edit serial_terminal.py manually
# Then rebuild
build_exe.bat
```

---

## Troubleshooting

### Issue: Version doesn't update in window title
**Solution**: Make sure you saved `serial_terminal.py` and rebuilt the package

### Issue: Old version still showing
**Solution**: 
- Clear Python cache: `rm -rf __pycache__`
- Reinstall package: `pip install -r requirements.txt`
- Restart application

### Issue: Version string format wrong
**Solution**: Use format `X.Y.Z` (e.g., `1.0.0`, `2.1.5`)

---

## Future Enhancements

Possible additions to version system:
- [ ] Automatic online version check
- [ ] Download links in update dialog
- [ ] Changelog display in app
- [ ] Auto-update feature
- [ ] Version migration tool

---

## Summary

Version management is now fully integrated:
- ✅ Version visible in window title
- ✅ Help menu with version options
- ✅ About dialog with features
- ✅ Update check with instructions
- ✅ Easy to update for new releases

**To release a new version:**
1. Change `APP_VERSION` and `APP_BUILD_DATE` in code
2. Rebuild packages
3. Done! Version appears everywhere automatically

---

**Last Updated**: October 7, 2026  
**Current Version**: 1.0.0  
**Status**: ✅ Ready for Use
