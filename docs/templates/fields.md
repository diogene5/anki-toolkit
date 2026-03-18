# Field Replacements

## Basic Replacements

Field names in Anki templates use curly bracket syntax. When you write `{{Front}}`, Anki searches for a field with that exact name and replaces it with the field's content. Field names are case sensitive. If you have a field named `Front`, writing `{{front}}` will not work properly.

Templates can include arbitrary text alongside field references. For example: `What's the capital city of {{Country}}?`

A typical back template uses: `{{FrontSide}}<hr id=answer>{{Back}}`. The `id=answer` attribute helps Anki scroll to the answer section on long cards.

## Newlines

Web-based templates require explicit line breaks. To create a new line, add `<br>` at the end of a line:

```
{{Field 1}}<br>
{{Field 2}}
```

## Text to Speech

Use the syntax `{{tts en_US:Front}}` to enable text-to-speech for individual fields. Multiple voices can be specified: `{{tts ja_JP voices=Apple_Otoya,Microsoft_Haruka:Field}}`. Speed adjustment is also possible: `{{tts fr_FR speed=0.8:SomeField}}`.

For multiple fields: `[anki:tts lang=en_US] Text and {{Field1}} {{Field2}}[/anki:tts]`

## Special Fields

Available special fields include:
- `{{Tags}}` - Note tags
- `{{Type}}` - Note type
- `{{Deck}}` - Card's deck
- `{{Subdeck}}` - Card's subdeck
- `{{CardFlag}}` - Card flag
- `{{Card}}` - Card type
- `{{FrontSide}}` - Front template content (back template only)

## Hint Fields

To create a hidden hint: `{{hint:MyField}}`

This displays a clickable link that reveals the field content. The hint resets when the answer is shown unless manually configured otherwise.

## Dictionary Links

Create searchable links using field replacement:

```
<a href="http://example.com/search?q={{text:Expression}}">check in dictionary</a>
```

The `text:` prefix removes HTML formatting from fields.

## HTML Stripping

Use the `text:` prefix to strip formatting: `{{text:Expression}}`

## Right-to-Left Text

```
<div dir=rtl>{{FieldThatHasRTLTextInIt}}</div>
```

## Ruby Characters (Furigana)

Format ruby text as: `Text[Ruby]`

Apply the `furigana` filter: `{{furigana:MyField}}`

Additional filters include:
- `{{kana:MyField}}` - Shows only ruby text
- `{{kanji:MyField}}` - Removes ruby text

## Media & LaTeX

Static media requires underscore-prefixed filenames:
```
<img src="_logo.jpg">
```

Field references in media tags are unsupported and should instead be included directly in the field content.

## Type-in-the-Answer Feature

Add `{{type:FieldName}}` to enable answer checking. For cloze cards: `{{type:cloze:Text}}`

To ignore diacritics: `{{type:nc:Front}}`

Advanced styling uses CSS classes: `typeGood`, `typeBad`, and `typeMissed`.
