# Installing & Upgrading Anki on Linux

## Requirements

The packaged version needs a recent 64 bit Intel/AMD Linux with glibc 2.36+, and common libraries like libwayland-client and systemd. Alternative installation methods exist for users on different architectures or minimal Linux distributions.

For Debian-based systems including Ubuntu, run this prerequisite command:

```
sudo apt install libxcb-xinerama0 libxcb-cursor0 libnss3
```

Users experiencing startup failures may need additional libraries. Ubuntu 24.04 users facing issues should consult the community forums. Note that musl-based distributions are not currently supported due to Anki's build system requirements.

## Installing

1. Download Anki from https://apps.ankiweb.net to your Downloads folder
2. Install zstd if needed: `sudo apt install zstd`
3. Open a terminal and execute:
   ```
   tar xaf Downloads/anki-2XXX-linux-qt6.tar.zst
   cd anki-2XXX-linux-qt6
   sudo ./install.sh
   ```
4. Start Anki by typing `anki` and pressing Enter

Some systems may require `tar xaf --use-compress-program=unzstd` instead.

## Upgrading

Remove previous system-installed versions before installing new packages. Upgrading preserves user data. Users wishing to downgrade should do so before updating to a newer version.

## Add-on Compatibility

Older Anki versions are available from the releases page for compatibility with add-ons that may not work with the latest version.

## System Qt Versions

Advanced users can configure Anki to use their system's Qt libraries instead of official PyQt builds. This requires Python 3.11+ and PyQt 6.2+.

Setup instructions:

1. Install Python and PyQt packages: `sudo apt install python3-pyqt6.qtwebengine`
2. Remove previous launcher files: `rm -rf ~/.local/share/AnkiProgramFiles`
3. Extract launcher and navigate to its folder
4. Create system_qt file: `touch system_qt`
5. Install via `./anki` or `./install.sh`

Note: This is experimental and may introduce unexpected behavior.

## Problems

For installation or startup issues, consult these resources:

- [Missing Libraries](missing-libraries.md)
- [Display Issues](display-issues.md)
- [Blank Main Window](blank-window.md)
- [Linux Distro Packages](distro-packages.md)
- [Incorrect GTK Theme](gtk-theme.md)
- [Wayland](wayland.md)
- [Input Methods](input-methods.md)
