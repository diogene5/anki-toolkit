# Text Files

## Overview

Any plain text file with fields separated by commas, semicolons, or tabs can be imported into Anki. Files must be plain text format (`.txt`) and UTF-8 encoded.

## Key Requirements

- **File Format:** Plain text only; convert `.xls`, `.rtf`, `.doc` files first
- **Encoding:** UTF-8 format required
- **Field Detection:** Anki determines field count from the first non-commented line
- **Separator Detection:** Anki auto-detects field separators (commas, tabs, etc.)

## Field Mapping

Fields in text files map to note fields during import, including tags. Users select which text file column corresponds to which note field.

## Newlines and Special Characters

Two methods handle newlines or field separators within fields:

**Quotation Marks (Escape Method):**
```
hello;"this is
a two line answer"
"this includes a ; (semicolon)";another field
```

To include quotes within quoted fields, use double quotes: `""escaped quotes""`

**HTML Newlines:**
```
hello; this is<br>a two line answer
```
Enable "Allow HTML in fields" in the import dialog.

## UTF-8 and Spreadsheets

LibreOffice is recommended over Excel for non-Latin characters. Export as CSV via **File > Save As**.

## HTML Support

When importing, checking "allow HTML in fields" enables formatted text (bold, italics). Use these replacements for special characters:

| Character | Replacement |
|-----------|-------------|
| < | `&lt;` |
| > | `&gt;` |
| & | `&amp;` |

## Media Importing

Place audio/image files in the `collection.media` folder (no subdirectories). Reference them in fields:

```
<img src="myimage.jpg">
[sound:myaudio.mp3]
```

Alternatively, use find & replace with regex pattern `(.*)` replaced with `[sound:\1.mp3]`.

## Bulk Media Import

The media import add-on automatically creates notes from folder files, displaying filenames on front and media on back.

## Duplicates and Updating

By default, Anki uses the first field to identify duplicates. Matching notes update automatically unless changed via dropdown options. The **match scope** setting controls whether duplicates are identified by note type alone or note type plus deck.

When updating is enabled, existing notes retain their current decks and scheduling information.

## File Headers

Anki 2.1.54+ supports `#key:value` headers at file start:

| Header | Values | Function |
|--------|--------|----------|
| `separator` | Comma, Semicolon, Tab, Space, Pipe, Colon | Sets field delimiter |
| `html` | true, false | Enables HTML processing |
| `tags` | Space-separated tags | Applies tags to all notes |
| `columns` | Column names | Names columns during import |
| `notetype` | Note type name/id | Presets note type |
| `deck` | Deck name/id | Presets deck |
| `notetype column` | 1, 2, 3… | Specifies note type column |
| `deck column` | 1, 2, 3… | Specifies deck column |
| `tags column` | 1, 2, 3… | Specifies tags column |
| `guid column` | 1, 2, 3… | Specifies GUID column |

### Special Columns

**Notetype Column:** Enables importing different note types with implicit field mapping.

**Deck Column:** Places cards in decks specified per row; creates decks if needed.

**GUID Column:** Uses Anki's unique identifiers for reliable duplicate detection during re-import. GUIDs are Anki-generated; custom IDs should go in the first field instead.
