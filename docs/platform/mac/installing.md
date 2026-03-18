# Installing & Upgrading Anki on macOS

## Requirements

macOS version requirements are available on the download page. For older machines, previous versions can be downloaded from the releases page. The Qt5 builds in version 24.11 and earlier support macOS 10.14 and later. For macOS versions between 10.10 and 10.13, Anki 2.1.35-alternate is recommended.

## Installing

1. Download Anki from https://apps.ankiweb.net
2. Save the file to your desktop or downloads folder
3. Open it and drag Anki to your Applications folder or desktop
4. Double-click on Anki in the location you placed it

## Upgrading

To upgrade, close Anki if running, then follow the installation steps above. Drag the Anki icon to the same location where it was previously stored. When prompted, overwrite the old version. Card data will be preserved during this process.

## Homebrew

Homebrew users can install Anki using:

```
brew install --cask anki
```

Upgrading is done with `brew upgrade`, and uninstalling uses `brew uninstall --cask anki`.

## Add-on Compatibility

Some add-ons may not function with the latest Anki release. If upgrading causes an essential add-on to stop working, older versions are available from the releases page.

## Problems

For installation or startup issues, consult the [Display Issues](display-issues.md) documentation.
