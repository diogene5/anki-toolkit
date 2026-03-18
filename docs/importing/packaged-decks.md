# Packaged Decks

## Overview

Anki packages (.apkg files) enable you to import decks, notes, note types, and cards from other users. These files are frequently distributed through AnkiWeb's shared deck collection.

## Scheduling

Packaged decks can include scheduling data, beneficial for transferring between devices. However, importing shared decks typically means users won't want the original author's intervals or review history.

If imported cards show unusually large intervals, the deck creator may have inadvertently included their scheduling data. Users can reset these through the Set Due Date feature or, in Anki 23.10+, by deselecting "Import any learning progress" during import. This also removes leech and marked tags.

## Updating

When importing .apkg files, Anki recognizes previously imported notes. If the notes in the file are newer than your local copy, the notes will be updated with the contents of the file by default.

Updating becomes problematic when note types are modified. Missing notes can still be imported, but previously imported notes won't update if the author made changes.

### Anki 23.10 and Later

This version increased flexibility with three options: unconditionally update notes (overwriting modifications), never update existing objects, or merge note type versions when both parties made changes. Merging preserves all templates and fields but requires full syncing.

#### Note to Deck Authors

Merging depends on template and field IDs (introduced in Anki 2.1.67). An add-on resource explains the advantages of sharing note types with these identifiers.
