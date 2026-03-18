# Display Issues on macOS

## Change the Video Driver

### Changing the Driver From the Preferences Screen

For Anki 23.10 and later, users experiencing display problems or crashes can adjust the video driver through the preferences menu. Navigate to **Anki > Preferences** and select a driver from the dropdown, then restart the application.

### Changing the Driver From Terminal.app

Earlier Anki versions required terminal access to modify the driver setting. Users can open Terminal.app and execute:

```
echo software > ~/Library/Application\ Support/Anki2/gldriver6
```

To revert to default settings, replace `software` with `auto` or delete the file entirely.

## eGPUs

External graphics cards on Mac systems may cause blank screen issues. This can be resolved by right-clicking the Anki application, selecting **Get Info**, and enabling the **prefer eGPU** option.

## Monitors with Different Resolutions

For issues related to multiple displays with varying resolutions, refer to the relevant community discussion on the Anki forums.
