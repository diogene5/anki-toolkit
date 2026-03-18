# Filtered Decks & Cramming

Filtered decks allow users to study outside normal Anki limits by creating temporary decks with custom filters. They're useful for test prep, focusing on specific material, and managing study backlogs.

## Custom Study

The Custom Study button provides preset filters for common tasks. It creates a "Custom Study Session" deck that automatically opens. The available options include:

- **Increase today's new card limit** – Add more new cards to your current deck (modifies existing deck rather than creating filtered deck)
- **Increase today's review card limit** – Show additional due reviews beyond daily limits
- **Review forgotten cards** – Display cards answered "Again" within a specified timeframe
- **Review ahead** – Show cards due in the near future
- **Preview new cards** – Study recently added cards without converting them to review cards
- **Study by card state or tag** – Select specific cards by status or tags

## Home Decks

Cards retain links to their original "home decks" when moved to filtered decks. They automatically return after studying, either after one review or multiple reviews depending on settings.

Two options exist for bulk returns:
- The "Empty" button returns all cards to home decks without deleting the filtered deck
- Deleting a filtered deck accomplishes the same thing while removing it from the deck list

## Creating Manually

Advanced users can create filtered decks using arbitrary search strings through Tools > Create Filtered Deck. The Build button gathers matching cards; the Rebuild button refetches using the same filters.

**Limitations:** Filtered decks cannot include suspended, buried, or cards already in other filtered decks.

The search area uses the same syntax as the browser. The limit option controls card quantity gathered, with order determining both gathering and review sequence.

## Order

The "cards selected by" option determines card appearance order:

- **Oldest seen first** – Longest time since last review
- **Random** – No set order
- **Increasing intervals** – Smallest interval first
- **Decreasing intervals** – Largest interval first
- **Most lapses** – Most failed cards first
- **Order added** – Earliest creation date first
- **Order due** – Earliest due date first
- **Latest added first** – Most recently added cards first
- **Relative overdueness** – Cards most likely forgotten first (considers interval length and overdue duration)

## Steps & Returning

Filtered decks use home deck learning steps by default. Cards return when relearning completes. With rescheduling disabled, four buttons appear: Again, Hard, Good (with configurable delays), and Easy (removes from filtered deck).

## Due Reviews

Due cards display with normal review options. Correct answers return cards to home decks with adjusted scheduling; incorrect answers trigger home deck relearning steps.

## Reviewing Ahead

Non-due cards receive special algorithm treatment accounting for review timing. Early reviews receive delays similar to scheduled timing, while immediate reviews maintain previous delays.

**Note:** "Review ahead" isn't suitable for repeated daily use, as it creates scheduling conflicts with newly learned material.

## Rescheduling

By default, cards return with altered scheduling based on performance. Disabling "Reschedule cards based on my answers" switches to preview mode, returning cards unchanged.

## Catching Up

For backlog management, users can create separate filtered decks using search filters like "is:due prop:due>-7" (recently due) and "is:due prop:due<=-7" (significantly overdue) to manage catch-up systematically.
