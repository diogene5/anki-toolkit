# Windows Display Issues

## Overview

On Windows, Anki offers three graphics rendering options. The default "software" mode prioritizes compatibility over speed, while "OpenGL" and "ANGLE" provide faster performance but may cause display problems like missing menubars or blank windows. The optimal choice depends on individual system configurations.

## Changing the Driver From the Preferences Screen

Users with Anki 23.10 and later can adjust the graphics driver through the settings interface by going to **Tools > Preferences** and selecting their preferred option from the available dropdown menu.

## Changing the Driver From the Command Line

For those experiencing display problems, switching to software rendering mode is possible via command line.

**Command Prompt method:**

```
echo software > %APPDATA%\Anki2\gldriver6
```

**PowerShell method:**

```
echo software > $env:APPDATA\Anki2\gldriver6
```

No output will appear after running either command. Restart Anki to apply the changes.

To restore default behavior, replace `software` with `auto` or remove the file entirely.

## Full Screen

Anki 2.1.50+ includes full screen functionality, though it was previously restricted when using OpenGL due to compatibility concerns. Enabling software rendering allows full screen use, though rendering speed may decrease as a result.

With Anki 23.10 and newer, full screen mode works with the standard Direct3D driver.
