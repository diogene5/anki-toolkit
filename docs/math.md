# Math and Symbols

## MathJax

[MathJax](https://www.mathjax.org) is a modern browser-based typesetting system for mathematical and chemical equations. It requires no additional software installation and is recommended for most users.

MathJax is supported in Anki 2.1+, AnkiMobile, and AnkiDroid 2.9+.

**To use MathJax:**

1. Type `\sqrt{x}` in a field
2. Select the text
3. Click the rightmost editor button and choose "MathJax inline"
4. Anki converts it to `\(\sqrt{x}\)`
5. Click **Cards…** to preview the equation

**Key points:**
- Use `\(` and `\)` for inline equations
- Use `\[` and `\]` for display equations
- Use Shift+Enter for newlines within expressions
- Anki includes built-in support for mhchem for chemical equations

### Customize MathJax

MathJax loads before card content, so customization requires specific syntax:

```
<script>
MathJax.config.tex['macros'] = {
    R: '{\\mathbb {R}}',
};
if (typeof is_already_run == 'undefined') {
  is_already_run = true
  MathJax.startup.getComponents();
}
</script>
```

Note: Anki has special logic for cloze deletions that may break with non-standard delimiters.

---

## LaTeX

LaTeX is a powerful typesetting system for mathematical formulas, chemical formulas, and musical notation. Anki generates images from LaTeX code for card review.

**Limitations:**
- Requires manual installation and setup
- Images generate only on desktop; mobile displays pre-generated images
- More complex than MathJax

### Security Warning

LaTeX can contain malicious commands affecting your computer. Recent Anki versions refuse to generate images by default.

To enable LaTeX:
- Go to Preferences and enable "Generate LaTeX images"
- **Warning:** Avoid enabling this if using shared decks, as authors could potentially access your system

No action needed for shared decks with pre-generated images.

### Assumed Knowledge

LaTeX support requires existing LaTeX knowledge and installation:

- **Windows:** MiKTeX
- **macOS:** MacTeX or BasicTeX
- **Linux:** distribution package manager
- Dvipng must also be installed

**macOS with BasicTeX:**
```
sudo tlmgr update --self; sudo tlmgr install dvipng
```

### Web/Mobile

Anki generates LaTeX images and stores them in the media folder. Web and mobile clients display existing images but cannot generate new ones.

To bulk-generate images: Go to **Tools > Check Media**, then sync.

### Example

Use `[latex][/latex]` tags to include LaTeX:

```
Does [latex]\begin{math}\sum_{k = 1}^{\infty}\frac{1}{k}\end{math}[/latex] converge?
```

**Shorthand syntax:**
- `[$]...[/$]` for inline formulas (replaces `\begin{math}...\end{math}`)
- `[$$]...[/$$]` for display formulas (replaces `\begin{displaymath}...\end{displaymath}`)

### Packages

Customize the LaTeX preamble to import packages. Access via **Add > Note Type Selection > Manage > Options**.

Modify the header from:
```
\documentclass[12pt]{article}
\usepackage{amssymb,amsmath}
```

To include custom packages (example with chemtex):
```
\usepackage{chemtex}
```

### Template Conflicts

As of Anki 2.1.20+, `{{field}}` text inside fields no longer causes conflicts. Older versions may require changing separators:

Change from:
```
{{latex field}}
```

To:
```
{{=<% %>=}}
<%latex field%>
```

### Cloze Conflicts

Cloze deletions use `}}` which conflicts with LaTeX. Workarounds:

**Option 1:** Add a space before LaTeX closing braces:
```
{{c1::[$]\frac{foo}{\frac{bar}{baz} }[/$] blah blah blah.}}
```

**Option 2:** Use HTML comments in HTML mode:
```
{{c1::[$]\frac{foo}{\frac{bar}{baz}<!-- -->}[/$] blah blah blah.}}
```

### Unsafe Commands

Anki prohibits commands like `\input` and `\def` to prevent malicious deck damage. To use these, add them to a system package and import it.
