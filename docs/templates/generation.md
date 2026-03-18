# Card Generation

## Reverse Cards

A video tutorial on [reversing cards is available on YouTube](http://www.youtube.com/watch?v=DnbKwHEQ1mA&yt:cc=on).

For bidirectional cards (such as "ookii" → "big" and "big" → "ookii"), use the "Basic (and reversed card)" note type to generate both directions automatically.

The "Basic (optional reversed card)" note type offers flexibility. It creates a forward card with just the first two fields filled. Adding text to the "Add Reverse" field (like "y") triggers generation of a reverse card; this field content never appears on cards.

## Card Generation & Deletion

Anki requires non-empty front sides to create cards. Empty fronts prevent card generation.

When editing notes, Anki automatically generates new cards if previously blank fields now contain content. However, Anki will not delete them immediately, as that could lead to accidental data loss. Use Tools → Empty Cards to remove empty cards manually.

Individual card deletion isn't possible since they regenerate during note editing. Instead, empty the relevant conditional fields and use the Empty Cards function.

Special fields or non-field text don't factor into generation — only actual field content.

## Selective Card Generation

Generate extra cards for specific material by adding a dedicated field. Include text (like "1") only on notes requiring the extra card, then use conditional replacement in the template to control generation based on that field.

## Conditional Replacement

Use conditional syntax to display content only when fields contain or lack text:

```
{{#FieldName}}
    Text shown if FieldName has content
{{/FieldName}}

{{^FieldName}}
    Text shown if FieldName is empty
{{/FieldName}}
```

Control card generation by wrapping the entire front template in conditionals, ensuring cards only generate when required fields are populated.

## Blank Back Sides

Card generation only examines front templates. A card generates if the front is non-empty, regardless of back content.

To prevent blank backs, place required fields as conditionals on the front template.

## Adding Empty Notes

When notes produce no cards, Anki creates a blank card using the first template. This enables adding incomplete material for later editing. Remove unwanted empty notes via the Empty Cards function.

## Cloze Templates

Cloze deletion note types function distinctly from regular types. Generation works as follows:

- The front template contains cloze replacements like `{{cloze:FieldName}}`
- The field contains cloze references like `{{c1::text}}`
- A card generates for each unique number

Cloze tags (`{{cloze:…}}`) only work with cloze note types, not regular ones.

Conditionals support special fields for rendering specific cloze cards, enabling hint display targeted to individual cloze numbers.
