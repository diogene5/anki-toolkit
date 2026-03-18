# Styling & HTML

## Card Styling

The styling section allows customization of card appearance through CSS properties. Key options include:

- **font-family**: Specify fonts (use quotes for multi-word names like `"MS Unicode"`)
- **font-size**: Set size in pixels
- **text-align**: Center, left, or right alignment
- **color**: Use color names or HTML codes
- **background-color**: Card background customization

Styling applies globally to all cards of a note type, though card-specific styling is possible using selectors like `.card1` for the first card.

## Image Resizing

By default, Anki shrinks images to fit screens. To disable this, add to your styling section:

```css
img {
  max-width: none;
  max-height: none;
}
```

For AnkiDroid compatibility, use `!important` directives. To exclude marked card stars from image resizing, target them with `img#star { ... }`.

## Field Styling

Apply different formatting to specific fields by wrapping them in HTML div tags with custom classes:

```html
<div class=mystyle1>{{Expression}}</div>
```

Then define the style in the styling section:

```css
.mystyle1 {
  font-family: ayuthaya;
  font-size: 30px;
}
```

## Audio Replay Buttons

Customize appearance of audio replay buttons using CSS targeting `.replay-button svg` elements for size, color, and styling properties.

## Text Direction

For right-to-left languages, add to the `.card` section:

```css
.card {
  direction: rtl;
}
```

Individual fields can be wrapped with `<div dir="rtl">{{Field}}</div>`.

## Other HTML

Templates support arbitrary HTML including tables, lists, images, and links, enabling complex card layouts beyond standard top/bottom arrangements.

## Browser Appearance

Define custom templates for the browser card list using the "browser appearance" option with standard template syntax, allowing simplified field display.

## Platform-Specific CSS

Apply different styles based on platform using special CSS classes like `.win`, `.mac`, `.linux`, `.mobile`, `.android`, and `.iphone`.

## Installing Fonts

Bundle fonts with decks without requiring system installation:

1. Rename font file with underscore prefix (e.g., `_arial.ttf`)
2. Add to the `collection.media` folder in your Anki profile
3. Reference in styling section:

```css
@font-face {
  font-family: myfont;
  src: url("_arial.ttf");
}
```

Supported formats include TrueType (.ttf), OpenType (.otf), and WOFF.

## Night Mode

Customize night mode appearance using `.card.nightMode` selector for global changes or `.nightMode .myclass` for specific elements.

## Fading and Scrolling

- Anki auto-scrolls to elements with `id=answer`
- Question fade-in delay adjustable via script (default 100ms)

## Javascript

Javascript can be embedded in card templates for advanced functionality. However, support is limited and testing across platforms is necessary. Use DOM manipulation methods like `createElement()` and `appendChild()` rather than direct write methods, as clients may dynamically update cards.
