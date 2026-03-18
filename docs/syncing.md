# Syncing with AnkiWeb

## Overview

AnkiWeb is a synchronization service that maintains collections across multiple devices and enables online studying. Users must create a free account before beginning.

## Setup Process

To initiate syncing, users click the sync button on the main screen or press Y. They'll enter their AnkiWeb credentials. On first sync, users choose to either upload their local cards or download from AnkiWeb. The manual notes: "If you have cards on your computer and your AnkiWeb account is empty, choose **Upload** to send your data to AnkiWeb."

## Automatic Syncing

Anki automatically synchronizes when collections open or close, though users can disable this in preferences for manual syncing instead.

## Sync Button Indicators

The sync button displays blue for standard syncs and red when a full sync is needed.

## Media Synchronization

Anki syncs sounds and images but "will not notice if you have made edits to existing files." Users must add, remove, or replace files to sync modifications. Media deletions only synchronize after full sync completion to prevent accidental data loss.

## Conflict Resolution

Most review and note edits merge successfully across devices. However, structural changes (adding fields, removing templates) require choosing which version to keep. The system can force one-way syncs using Tools > Preferences > Network settings.

## Merging Conflicts

When different content exists on multiple devices before syncing setup, manual merging is possible through exporting decks as `.apkg` files and importing them later.

## AnkiWeb Data Deletion

Inactive accounts (no access for 6 months) may have data deleted. The service sends warning emails before deletion occurs, allowing 30 days to reactivate by logging in or syncing.

## Network Configuration

### Firewall Requirements

Anki requires outbound HTTPS connections to ankiweb.net and related domains. Wildcard access to `*.ankiweb.net` is recommended.

### Proxy Settings

System proxies are automatically detected on Windows/macOS. For other systems or manual configuration, users define an `HTTPS_PROXY` environment variable with format:

```
http://user:pass@proxy.company.com:8080
```

Special characters like @ in credentials require URL encoding as %40.
