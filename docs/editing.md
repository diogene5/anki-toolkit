# Adding/Editing

## Adding Cards and Notes

In Anki, users add notes rather than cards; the software automatically generates cards. Access the Add Notes window by clicking **Add** in the main window.

The interface displays the current note type (typically "Basic") and the destination deck. Fields labeled "Front" and "Back" can be customized via the "Fields..." button. Users can attach tags to notes by entering space-separated labels in the tags area.

After completing the fields, click **Add** or press Ctrl+Enter (Cmd+Enter on Mac) to save the note.

### Duplicate Check

Anki checks the first field for uniqueness, so it will warn you if you enter two cards with a Front field of "apple" (for example). The check applies only to the current note type. Users can run the browser's "Find Duplicates" function to identify duplicates in other fields.

### Effective Learning

Two key principles are recommended:

- **Keep it simple**: Shorter cards are easier to review and prevent context-dependent learning
- **Don't memorize without understanding**: Learn language in context and understand concepts before memorizing details

## Adding a Note Type

Access this feature via **Tools > Manage Note Types**. Users can create new types by selecting "Add" (based on built-in types) or "Clone" (based on existing collection types). This enables organizing multiple pieces of information across separate fields rather than cramming content together.

## Customizing Fields

Click the **Fields...** button to add, remove, or rename fields. The reposition button allows adjusting field order numerically, or drag fields directly to reorder them.

Key field options include:

- **Editing Font**: Customize display font for note editing
- **Sort by this field**: Show this field in the browser's sort column
- **Reverse text direction**: For right-to-left languages
- **Use HTML editor by default**: Direct HTML editing preference
- **Collapse by default**: Automatically collapse fields
- **Exclude from unqualified searches**: Hide field content from general searches

Do not use reserved names: "Tags", "Type", "Deck", "Card", or "FrontSide".

## Changing Deck / Note Type

Click the top buttons while adding notes to change the note type or deck. The resulting window permits both selection and creation of new decks or management of note types.

## Organizing Content

### Using Decks Appropriately

Decks should represent broad study categories. Creating numerous small decks is discouraged because it may cause cards to appear in recognizable sequences, reducing learning effectiveness and potentially causing performance slowdowns.

### Using Tags

Tags offer advantages over decks for organization. Since each card can have multiple tags, you can do things like search for all verbs, or all food-related vocabulary, or all verbs that are related to food. Tags work at the note level, affecting all sibling cards.

### Using Flags

Flags resemble tags but appear during review as colored icons and work at the card level (affecting only individual cards, not siblings). Users can flag cards via Ctrl+1-7 (Windows) or Cmd+1-7 (Mac) during review or from the Browser. Only one flag per card is permitted.

### The "Marked" Tag

Anki treats a tag called "marked" specially, displaying a star on the study screen and highlighting marked notes in the browse screen. This feature exists mainly for compatibility with older versions; flags are generally recommended instead.

### Using Fields

Add organizational fields like "book" or "page" to classify content. Anki supports field-specific searches, enabling queries like `"book:my book" page:63`.

### Custom Study and Filtered Decks

Create temporary decks from search terms using custom study and filtered decks. This allows reviewing mixed content normally while creating focused study sessions when needed for specific topics or exams.

## Editing Features

The editor appears when adding notes, editing during reviews, or browsing. Top buttons access fields and cards windows. Right-side buttons control:

- Text formatting (bold, italic, underline)
- Subscript and superscript
- Text color
- Formatting removal
- Lists, alignment, and indentation
- Media attachment (audio, images, videos)
- Audio recording via microphone
- MathJax/LaTeX shortcuts
- HTML editing

Sticky fields (available in Anki 2.1.45+) prevent field clearing after adding a note. Click the pin icon to toggle this feature.

When pasting, Anki preserves formatting by default. Hold Shift while pasting to strip formatting. This behavior can be toggled in Preferences.

## Cloze Deletion

Cloze deletion hides words within sentences. For example: "Canberra was founded in 1913" becomes "Canberra was founded in [...]."

Select the Cloze note type and enter text in the "Text" field. Highlight text to hide and click the [...] button. Anki replaces the selection with `{{c1::text}}` format, where "c1" indicates the deletion number.

Multiple deletions create multiple cards. For example: `{{c1::Canberra}} was founded in {{c1::1913}}` creates one card with both blanks, while `{{c1::Canberra}} was founded in {{c2::1913}}` creates two cards.

Custom hints can be added: `{{c1::Canberra::city}}` displays "[city]" as a hint during review.

Nested cloze deletions are supported (Anki 2.1.56+), though nesting is limited to approximately 3 levels in Anki 24.11 and 8 levels in other versions.

The default Cloze note type includes an "Extra" field for additional information displayed on the answer side.

## Image Occlusion

Image Occlusion (IO) notes hide image sections, testing knowledge of hidden content. Available in Anki 23.10+.

### Adding an Image

Open the Add screen, select "Image Occlusion" as the note type, then click **Select Image** or **Paste image from clipboard**.

### Adding IO Cards

After loading an image, use the left-side icons to add shapes (Rectangle, Ellipse, Polygon). Choose between two modes:

- **Hide All, Guess One**: All areas hidden; reveal one at a time
- **Hide One, Guess One**: One area hidden; others visible

The default IO note type includes Header, Back Extra, and Comments fields. Click **Toggle Mask Editor** to access these fields and tags from the IO editor.

## Editing IO Notes

Edit IO notes via "Edit" during review or from the browser. Available tools include:

- **Select**: Modify, group, or delete shapes
- **Zoom**: Navigate and zoom the image
- **Shapes**: Add new rectangles, ellipses, or polygons
- **Text**: Add non-card text areas
- **Undo/Redo**: Revert changes
- **Toggle Translucency**: Temporarily view hidden areas
- **Delete**: Remove shapes (cards must be deleted separately)
- **Duplicate**: Copy shapes
- **Group/Ungroup**: Create or break shape clusters
- **Alignment**: Position shapes and text

During review, a "Toggle Masks" button appears below the image in "Hide All, Guess One" mode.

## Inputting Non-Latin Characters and Accents

Modern computers support typing accents and non-Latin characters through keyboard layouts. The recommended method is using language-specific keyboard layouts.

### Adding International Keyboard Layouts

Instructions vary by operating system:

- **Windows**: Search for "US International keyboard" setup guides
- **Mac**: Use System Preferences to add international keyboard layouts
- **Linux**: Refer to distribution-specific wikis (Arch Linux, Debian, etc.)

### Adding Keyboard Layouts for Specific Languages

Language-specific keyboards are added similarly. Search online for language-specific input methods (e.g., "input Japanese on a mac", "type Chinese on Windows 10").

### Right-to-Left Languages

Learning right-to-left languages requires additional considerations. Consult external resources for detailed guidance.

### Limitations

Anki's toolkit struggles with certain input methods, including macOS key-hold accent selection and Windows Alt+numeric code input.

## Unicode Normalization

Text like "a" can be represented multiple ways (specific code versus "a" plus accent code). This causes search mismatches when mixing sources. Anki normalizes text to standard form automatically, though this may convert archaic characters (like old Japanese symbols) to modern equivalents.

To disable normalization, enter in the debug console:

```
mw.col.conf["normalize_note_text"] = False
```

Content added afterward remains untouched, but cross-platform searching may become difficult.
