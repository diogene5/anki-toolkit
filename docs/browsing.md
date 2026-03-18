# Browsing

## Overview

The Browse window enables searching and editing of cards and notes, accessible via the **Browse** button or keyboard shortcut B. It comprises three sections: sidebar (left), card/note table (top right), and editing area (bottom right). Users can resize sections by dragging dividers between them.

## Table Modes

Anki 2.1.45+ offers two display modes toggled via a switch near the search area or Ctrl+Alt+T (Cmd+Opt+T on Mac):
- **Cards mode**: Shows individual cards
- **Notes mode**: Displays notes

## Sidebar

The left sidebar provides quick access to common search terms and includes:

### Search Tool

Clicking items searches for them. Modifier keys enable:
- **Ctrl/Cmd + click**: Append to current search with AND logic
- **Shift + click**: Create OR search
- **Alt/Option + click**: Negate search (prepend `-`)
- **Ctrl+Shift + click**: Replace all occurrences of the same search type

### Selection Tool

Allows selecting multiple items via Ctrl/Shift clicking and enables drag-and-drop reordering of decks and tags. Right-click selections to choose "Search > All/Any Selected."

### Saved Searches

Right-click the topmost sidebar item and select "Save Current Search" to store frequently-used searches. Drag sidebar items to this area to pin them.

### Editing Items

Delete or rename tags, decks, and saved searches via right-click menu or shortcuts (Del and F2 on Windows). Multiple items can be deleted simultaneously.

### Finding Items

Type part of an item's name in the sidebar's searchbar to locate it.

## Search Box

Above the card list sits a search box for entering search queries. Detailed search syntax is documented in the Searching section.

## Card/Note Table

Table rows represent cards or notes matching the current search. Clicking a row displays the corresponding note in the editing area below.

### Rows

Multiple rows can be selected by dragging, holding Ctrl, or Command. The editor hides when multiple selections occur. Most operations work on selected items, while some (like card information) operate only on the "current" card/note—typically the last clicked or selected item.

Background colors indicate card/note status (in Cards mode, first match applies):
- **Flagged**: Flag color
- **Suspended**: Yellow
- **Marked note**: Purple

### Columns

Right-click column headers (Ctrl+click on Mac) to configure visible columns. Columns are draggable for reordering. Click column headers to sort; click again to reverse order. Question and Answer columns cannot be sorted.

Available columns differ slightly between modes:

| Column | Cards Mode | Notes Mode |
|--------|-----------|-----------|
| Answer | Back side in one line | Same as Cards mode, first card only |
| Card(s) | Template name | Number of cards |
| Card Modified | Last card changes | Last changes to any card |
| Created | Same as Notes mode | Note creation date |
| Deck | Card's deck name | Number of decks or single deck name |
| Due | Review/learning due date or new queue position | Next due review/learning card |
| Ease | Card's ease (if not new) | Average ease across cards |
| Interval | Card's interval | Average interval across cards |
| Lapses | "Again" count | Total lapses across cards |
| Note | Same as Notes mode | Note type name |
| Note Modified | Same as Notes mode | Last content edit |
| Question | Front side in one line | Same as Cards mode, first card only |
| Reviews | Review count | Total reviews across cards |
| Sort Field | Same as Notes mode | Note type's sort field content |
| Tags | Same as Notes mode | Note's tags |

## Editing Area

The bottom right displays the currently selected note's editing interface. Click the **Preview** button to see how the card appears during review (type-the-answer fields are hidden for quick preview).

## Menus and Actions

### Edit Menu

| Action | Description |
|--------|-------------|
| Undo | Revert the most recent operation |
| Select All | Select all displayed rows |
| Select Notes | Show only selected notes with all rows selected |
| Invert Selection | Toggle selection status of all rows |
| Create Filtered Deck | Open filtered deck dialog with current search as filter |

### Notes Menu

| Action | Description |
|--------|-------------|
| Add Notes | Open the Add dialog |
| Create Copy | Duplicate current note in editor for variations |
| Export Notes | Open Export dialog |
| Add Tags | Add tags to selected notes |
| Remove Tags | Remove specified tags from selected notes |
| Clear Unused Tags | Remove unused tags from sidebar |
| Toggle Mark | Mark/unmark selected notes |
| Change Note Type | Convert notes between types |
| Find Duplicates | Open Duplicates dialog |
| Find and Replace | Open Find and Replace dialog |
| Manage Note Types | Open Note Types dialog |
| Delete | Remove selected notes and cards |

### Cards Menu

| Action | Description |
|--------|-------------|
| Change Deck | Move selected cards to different deck |
| Set Due Date | Convert new cards to review or reschedule review cards. Range syntax (e.g., `60-90`) sets due date within that interval; `!` forces interval reset |
| Reset | Move cards to new queue end while preserving review history. Anki 2.1.50+ offers options to restore original position and reset counters |
| Reposition | Change new card order. Multiple selections receive increasing position numbers; "Shift position of existing cards" inserts cards between existing ones without overlap |
| Toggle Suspend | Suspend or unsuspend selected cards |
| Flag | Toggle flags on selected cards |
| Info | Display card information including review history |

### Go Menu

Provides keyboard shortcuts to navigate browser sections and move through the card list.

## Find and Replace

This dialog replaces text across notes. Users specify:
- Text to replace
- Replacement text
- Search location: tags, all fields, or specific field
- Scope: selected notes only (default) or all notes

The **Regular expression** option enables complex replacements using pattern matching syntax. For Anki 2.1.28+, see the [regex documentation](https://docs.rs/regex/latest/regex/index.html#syntax); older versions use [Python's re module](http://docs.python.org/library/re.html).

## Finding Duplicates

The "Notes > Find Duplicates" feature identifies notes with identical content. Users:
1. Select a field from the dropdown
2. Click **Search** to find duplicates across all matching note types
3. Optionally use the **Optional filter** text box to narrow results (e.g., `"note:french vocab" or "note:french verbs"`)

Search syntax matches browser search conventions. Click result links to display duplicates, or use **Tag Duplicates** to tag matches for batch handling.
