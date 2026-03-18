# Self-Hosted Sync Server

## Overview

Advanced users who prefer not to use AnkiWeb can deploy their own sync server. Key considerations include:

- This requires comfort with networking and command-line tools
- Client updates may require corresponding server updates to maintain compatibility
- Third-party alternatives exist but lag behind official protocol changes
- UI messages reference "AnkiWeb" regardless of custom server configuration

## Installation Methods

### Packaged Build (Anki 2.1.57+)

**Windows:**
```
set SYNC_USER1=user:pass
"\Program Files\anki\anki-console" --syncserver
```

**macOS:**
```
SYNC_USER1=user:pass /Applications/Anki.app/Contents/MacOS/launcher --syncserver
```

**Linux:**
```
SYNC_USER1=user:pass anki --syncserver
```

### Python Package

Requires Python 3.9+:
```
python3 -m venv ~/syncserver
~/syncserver/bin/pip install anki
SYNC_USER1=user:pass ~/syncserver/bin/python -m anki.syncserver
```

### Rust Implementation (2.1.66+)

Requires Rustup and Protobuf:
```
cargo install --locked --git https://github.com/ankitects/anki.git --tag 25.02.5 anki-sync-server
SYNC_USER1=user:pass anki-sync-server
```

### Docker

User-contributed Dockerfile available in the Anki repository documentation folder.

## Configuration

**Multiple Users:** Set `SYNC_USER1`, `SYNC_USER2`, etc., with username:password format

**Hashed Passwords:** Generate hashes using external tools, set `PASSWORDS_HASHED=1`

**Storage:** Define `SYNC_BASE` environment variable (default: ~/.syncserver)

**Network:** Configure `SYNC_HOST` and `SYNC_PORT`

**Request Size:** Adjust `MAX_SYNC_PAYLOAD_MEGS` if needed (default 100MB)

## Security & Access

The server uses unencrypted HTTP; implement HTTPS via reverse proxy or VPN. Restrict local network access or use encryption layers like Tailscale.

## Client Configuration

Enter your server's network address in Anki preferences (e.g., `http://192.168.1.200:8080/`).

iOS users may need to enable local network access in Settings.

Legacy clients require separate `SYNC_ENDPOINT` and `SYNC_ENDPOINT_MEDIA` configuration.

## Reverse Proxy Notes

Include trailing slashes in custom paths. iOS requires TLS 1.2 support.
