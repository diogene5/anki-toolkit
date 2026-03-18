# Windows Startup Issues

## No error, but app does not appear

When Anki starts without displaying the application, try these solutions:

- Disconnect multiple or external displays
- Install the latest Anki version from https://apps.ankiweb.net
- Adjust your decimal separator setting if it isn't a period
- Install the older 2.1.35-alternate build

## Windows updates

Common startup error messages include:

- "Error loading Python DLL"
- "The program can't start because api-ms-win.... is missing"
- "Failed to execute script runanki"
- "Failed to execute script pyi_rth_multiprocessing"
- "Failed to execute script pyi_rth_win32comgenpy"

These typically result from missing Windows updates or libraries. Open Windows Update to ensure all updates are installed, then restart your device if needed.

## Windows 7/8

Manual installation of additional updates may be required:

- https://www.microsoft.com/en-us/download/details.aspx?id=48234
- https://aka.ms/vs/15/release/vc_redist.x64.exe
- http://www.catalog.update.microsoft.com/Search.aspx?q=kb4474419
- http://www.catalog.update.microsoft.com/Search.aspx?q=kb4490628

## Video driver issues

Refer to the [display issues](display-issues.md) documentation.

## Multiple displays

A LoadLibrary error 126 may occur due to toolkit compatibility with multiple displays.

## Antivirus/firewall software

Third-party security software might prevent Anki from loading. Try adding an exception for Anki or temporarily disabling security software.

## Admin access

Run Anki as administrator by right-clicking the icon and selecting "Run as administrator."

## Multiple Anki installations present after updating

If multiple Anki installations exist (such as in both Program Files and Program Files (x86)), uninstall all copies through Windows Settings, then reinstall.

## Debugging

Launch Command Prompt and run:

```
%LocalAppData%\Programs\Anki\anki-console.bat
```

Terminal output may reveal error details.

## If all else fails

Two remaining options exist:

- Run Anki from Python
- Install an older version like 2.1.35-alternate or 2.1.15
