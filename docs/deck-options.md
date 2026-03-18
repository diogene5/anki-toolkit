# Deck Options

## Overview

Deck options in Anki primarily control card scheduling. The manual recommends spending several weeks with default settings before making adjustments, emphasizing the importance of understanding options before changes. Access deck options via the gear icon, Options button, or keyboard shortcut O.

## Presets & Subdecks

Options group into presets that can be shared across decks. Subdecks can use different presets, allowing customized settings per deck level. When studying a subdeck, that subdeck's options apply to its cards, while display order comes from the parent deck selected for study.

## Daily Limits

- **New cards per day**: Controls daily introduction rate; limits reset each day
- **Maximum reviews**: Sets upper bound on daily review cards
- **Per-deck limits**: Options include preset-wide, deck-specific, or temporary (today only) limits
- **New Cards Ignore Review Limit**: When enabled, new cards display regardless of review limit
- **Limits Start From Top**: Makes parent deck limits apply to subdecks when selected

## New Cards

Learning steps control repetition frequency and spacing. The Hard button behavior varies by step position. Cards graduating move to review status based on "graduating interval." Easy button immediately graduates cards using the "easy interval" delay.

## Lapses

When failing review cards (pressing Again), relearning steps apply before cards return to review status. "Minimum interval" sets the shortest delay post-relearning, defaulting to one day.

## Display Order

Controls card gathering and sorting:

- **New card gather order**: By deck, random notes, position, or completely random
- **New card sort order**: By card type, randomly, or various combinations
- **Review sort order**: By due date, interval, ease, or overdueness

## FSRS (Free Spaced Repetition Scheduler)

An alternative to legacy SM-2 algorithm emphasizing accurate forgetting prediction. Key settings include:

- **Desired retention**: Probability of recalling cards when due (default 90%)
- **Parameters optimization**: Uses machine learning on review history
- **Compute minimum recommended retention**: Calculates optimal retention value

FSRS requires learning steps under 1 day and recommends against the Hard button for forgotten cards.

## Advanced Options

- **Maximum interval**: Caps review delays (default 100 years)
- **Historical retention**: Fills gaps in review history (default 90%)
- **Starting ease**: Initial multiplier for interval growth (default 2.50)
- **Easy bonus**: Extra multiplier for Easy responses (default 1.30)
- **Interval modifier**: Global review frequency adjuster
- **Custom scheduling**: JavaScript control for advanced users

The manual includes formulas and examples for calculating appropriate interval modifiers based on retention goals.
