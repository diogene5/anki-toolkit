# Getting Started

## Installing & Upgrading

The Anki ecosystem consists of Anki, AnkiMobile, AnkiDroid, and AnkiWeb. Installation instructions are available for Windows, Mac, and Linux platforms via the official website.

## Videos

Introductory videos covering core concepts:

- Shared Decks and Review Basics
- Syncing
- Switching Card Order
- Styling Cards
- Typing in the Answer

## Key Concepts

### Cards

A question and answer pair is called a _card_. It's similar to a paper flashcard with a question on the front and answer on the back. Users rate their recall accuracy, and Anki schedules subsequent reviews based on performance.

#### Card States

- **New:** Never studied cards
- **Learning:** Recently first-seen cards still being learned
- **Review:** Completed learning cards shown after delays
  - Young: interval < 21 days
  - Mature: interval >= 21 days
- **Relearn:** Forgotten review cards

### Decks

A _deck_ is a group of cards. Decks organize content hierarchically using double colons (e.g., `Chinese::Hanzi`). Each deck has customizable settings for daily limits and review intervals. The Default deck captures orphaned cards.

### Notes & Fields

Notes separate related information into structured fields. This approach enables creating multiple cards from one note -- useful for bidirectional language learning -- while tracking performance separately and allowing customized layouts.

### Card Types

_Card types_ function as templates determining which fields appear on question/answer sides. Templates use double-bracket syntax like `{{FieldName}}` for field replacement, enabling consistent formatting across cards.

### Note Types

Anki provides standard note types:

- **Basic:** Single front-to-back card
- **Basic (and reversed card):** Bidirectional cards
- **Basic (optional reversed card):** Conditional reverse card
- **Basic (type in the answer):** Manual answer entry with comparison
- **Cloze:** Text deletion exercises
- **Image Occlusion:** Image-based cloze deletions

Custom note types can be created via Tools > Manage Note Types.

### Collection

Your _collection_ is all the material stored in Anki: your cards, notes, decks, note types, deck options, and so on.

## Shared Decks

Downloading shared decks involves clicking "Get Shared," selecting a deck, and downloading the package for import. However, creating your own deck is the most effective way to learn a complex subject, as shared decks lack contextual explanation that complex topics require.
