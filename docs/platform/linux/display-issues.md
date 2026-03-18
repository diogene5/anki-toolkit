# Display Issues on Linux

Hardware acceleration is enabled by default. Users experiencing blank screens or display problems may resolve these issues by switching to software rendering.

## Changing the Driver From the Preferences Screen

In Anki 23.10 and later versions, users can modify the graphics driver through the preferences interface. Navigate to **Tools > Preferences** and select your preferred driver from the available dropdown options.

## Changing the Driver From the Terminal

Execute the following command:

```
echo software > ~/.local/share/Anki2/gldriver6
```

To revert to the default behavior, replace `software` with `auto` or delete the file entirely.
