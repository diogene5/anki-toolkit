# Checks and Errors

## Basics

Anki 2.1.45+ performs error checking when saving note types or exporting decks. These validations prevent issues during studying.

To modify a note type:
1. Open the Browse screen
2. Locate the note type in the left panel
3. Click the note type to display its cards
4. Click "Cards…" to access the templates screen

## Specific Issues

### Template Syntax Error

This occurs from incorrect field replacement syntax. Corrections update all cards using that template.

**Common errors:**

- **"Found '{{Field}}', but there is no field called 'Field'"** — Remove the non-existent field reference from the template.

- **"Missing }} in {{Field"** — Add closing braces: change `{{Field` to `{{Field}}`.

- **"Missing {{/Field}}"** — Add the missing closing tag for conditional replacements like `{{#Field}}` or `{{^Field}}`.

- **"Found {{/One}}, but expected {{/Two}}"** — Close conditional blocks in the same order they open.

- **"Found {{/Field}}, but missing '{{#Field}}' or '{{^Field}}'"** — Remove unmatched closing tags.

### Identical Front Sides

Duplicate card types create redundant questions, increasing workload and reducing scheduling efficiency. Remove duplicates by opening the templates screen, selecting the duplicate, and using the removal button.

### Front of Card is Blank

This indicates template fields lack content or required fields aren't included on the front template. Verify at least one populated field appears on the front template. For Cloze notes, include cloze deletions like `{{c1::text}}`.

### No Cloze Filter on Cloze Note Type

Cloze templates require cloze filters. Each cloze number generates a separate card.

**Single empty cards:** Editing text may create blank cards if cloze numbers change or disappear. Use the Empty Cards function (Tools menu) to remove them.

**All cloze cards empty:** If templates were modified, replace front and back text with `{{cloze:Text}}`, substituting your field name for "Text".
