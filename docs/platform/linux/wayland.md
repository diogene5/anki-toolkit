# Wayland

Users can activate Wayland support by setting the environment variable `ANKI_WAYLAND=1` before launching Anki (available since version 2.1.48).

## Benefits and Limitations

Wayland may give you better rendering across multiple displays, but it is currently off by default due to specific issues:

- Windows appear without borders on certain Linux distributions
- Window focus cannot be brought to the front, meaning actions like clicking Add to reveal an existing Add Cards window won't function as expected

These rendering challenges are the primary reason Wayland remains disabled by default despite its potential advantages for multi-display setups.
