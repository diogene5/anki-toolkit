# Media

Anki maintains sounds and images in a folder adjacent to the collection. When adding media through the editor or pasting into fields, Anki copies files from their original location to the media folder, simplifying backup and transfers.

Special characters in filenames (spaces, percentage signs) appear differently in the HTML editor than on disk. For example, `hello 100%.jpg` displays as `hello%20100%25.jpg` in the editor. Internally, Anki still uses the original filenames, so if you would like to search for the file or modify the filename with Find&Replace, you will need to use the name as it appears on disk, not as it appears in the HTML editor.

## Checking Media

The Tools>Check Media menu option scans notes and the media folder, identifying:
- Unused files in the media folder
- Missing media referenced in notes

This feature allows users to:
- Delete unused media files
- Tag notes with missing media references
- Empty the trash folder
- Restore deleted files

The tool excludes question and answer templates from scanning. Files prefixed with an underscore (like `_dog.jpg`) are ignored during checks. Deleted media moves to the operating system's trash for recovery if needed.

## Manually Adding Media

When adding media through Anki's interface, the application handles filename encoding for cross-device compatibility and removes incompatible characters. Manual additions to the media folder require running Tools>Check Media to ensure proper encoding before syncing.

Symbolic links in the media folder are not followed during syncing and may fail on mobile. Copy actual files into the collection.media folder instead of using symlinks.

## Supported Formats

Anki uses mpv (with mplayer fallback) for sound and video support. A wide variety of file formats are supported, but not all of these formats will work on AnkiWeb and the mobile clients. MP3 audio and MP4 video seems to be the most universally supported.
