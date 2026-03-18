# Backups

## Automatic backups

Anki generates automatic backups containing "the text on your cards and your scheduling information, but do not include sounds or image files." These serve as recovery tools for mistakes, though they shouldn't be relied upon as sole protection since they're stored locally and won't help if a device is lost or stolen.

### Restoring

To recover from an automatic backup:
1. Open Anki and select Switch Profile from the File menu
2. Click "Open Backup"
3. Choose your desired backup

**Important:** Restoring disables automatic syncing and backups temporarily. Reopen Anki after recovery to resume normal operations.

### Creating

Backups occur automatically every 30 minutes by default (configurable in preferences). Certain actions trigger immediate backups:
- One-way sync downloads
- Importing .colpkg files via File>Import
- Tools>Check Database

Anki removes backups older than two days, with user control over daily, weekly, and monthly retention.

## Manual colpkg backups

### Restoring

Use File>Import to restore from manual backups.

### Creating

In Anki 2.1.50+, access File>Create Backup for immediate backups. For backups including media files, select File>Export, choose "Anki collection package (.colpkg)", and enable "include media." Store the resulting file securely on another device or cloud storage.

## AnkiWeb

Syncing with AnkiWeb provides protection against device loss. Force a one-way sync through preferences or sync from a new device selecting "Download."

## Deletion log

Deleted notes are logged to deleted.txt in your profile folder, readable via File>Import, though imports support single note types only.
