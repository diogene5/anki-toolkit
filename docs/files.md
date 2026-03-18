# Managing Files and Your Collection

## Checking Your Collection

Anki includes a database check feature accessible via Tools>Check Database menu. This function verifies file integrity, rebuilds internal structures, and optimizes performance. The tag list is also rebuilt during this process, allowing users to remove unused tags that Anki doesn't automatically update when cards or decks are deleted. "Anki will automatically optimize your collection once every 2 weeks," though this automatic optimization doesn't check for errors or rebuild tags.

## User Data

Storage locations vary by operating system:

**Windows**: Latest versions store collections in `%APPDATA%\Anki2`, while older versions used a Documents folder called `Anki`.

**macOS**: Recent versions use `~/Library/Application Support/Anki2`. The Library folder is hidden by default but accessible by holding Option while clicking the Go menu in Finder.

**Linux**: Recent versions store data in `~/.local/share/Anki2` or `$XDG_DATA_HOME/Anki2` for custom paths. Flatpak builds use `~/.var/app/net.ankiweb.Anki/data/Anki2/`.

Each profile folder contains `collection.anki2` (notes, decks, cards), a `collection.media` folder, backups, and system files. "You should never copy or move your collection while Anki is open," as this risks corruption.

## Program Files

Anki's launcher installs to:
- Windows: `%LOCALAPPDATA%\Programs\Anki`
- macOS: `/Applications/Anki.app`
- Linux: `/usr/local/share/anki`

Support files download to AnkiProgramFiles directories. The AnkiProgramFiles folder can be copied and run from alternate locations using `AnkiProgramFiles/.venv/bin/anki` (Windows: `.venv\scripts\anki`).

## Startup Options

Safe mode disables syncing and add-ons by holding Shift during startup. Custom folder locations use: `anki -b /path/to/anki/folder`

Additional options include:
- `-p <name>`: Load specific profile
- `-l <iso 639-1 code>`: Change interface language

Windows shortcuts can be modified to include `-b` flags. The `ANKI_BASE` environment variable provides an alternative to command-line arguments.

## DropBox and File Syncing

Direct syncing of Anki folders with third-party services risks database corruption. For media-only syncing, external folder linking is recommended. For full collection synchronization, create scripts that copy files locally, launch Anki, then sync after closure to prevent corruption during file access.

## Network Filesystems

"We strongly recommend you have Anki store your files on a local hard disk, as network filesystems can lead to database corruption." Regular database checks are recommended if network storage is necessary.

## Running from a Flash Drive

Windows users can create portable USB installations. The drive letter must remain consistent across devices. FAT32 formatting may prevent media syncing; NTFS formatting is recommended.

Setup involves:
1. Installing the launcher to `E:\Anki\Launcher`
2. Creating an `Anki.bat` file with environment variables
3. Running the batch file to install Anki normally

## Backups

Backup information is referenced in a separate section.

## Inaccessible Harddisk

If Anki cannot write to its folder, a startup error appears. File permission issues require technical assistance to resolve.

## Permissions of Temp Folder

Incorrect temporary folder permissions prevent Anki operation. Windows 7 users should verify ownership and full control through the security tab in folder Properties.

## Corrupt Collections

Anki uses a crash-resistant format but corruption can occur when files are modified during operation, stored on network drives, or affected by bugs. Recovery prioritizes restoring from automatic backups.

Manual repair requires sqlite3 (pre-installed on macOS, downloadable for Windows).

**Linux/macOS procedure**:
```
sqlite3 collection.anki2 .dump > dump.txt
```
Edit dump.txt to change final "rollback;" to "commit;" if necessary, then:
```
cat dump.txt | sqlite3 temp.file
```

**Windows procedure**: Uses identical commands via command prompt (cmd.exe), replacing `cat` with `type`.

**Final step**: Verify temp.file isn't empty, rename original collection.anki2, rename temp.file to collection.anki2, move it to the collection folder, and run Tools>Check Database to confirm restoration.
