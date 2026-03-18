# Searching

## Overview

Anki's Browse screen and Filtered Deck feature utilize a unified search method for locating specific cards and notes. This search functionality can also adjust FSRS optimization scope.

## Simple Searches

Basic text searches match across all note fields. Key syntax includes:

- `dog cat` - finds notes containing both terms
- `dog or cat` - matches either term
- `-cat` - excludes notes with "cat"
- `"a dog"` - exact phrase matching
- `d_g` - single character wildcard
- `d*g` - zero or more character wildcard
- `w:dog` - word boundary search (exact word only)

Multiple search terms default to AND logic. Searches are case-insensitive for Latin characters.

## Field-Specific Searches

Limit searches to particular fields:

- `front:dog` - exact field match
- `front:*dog*` - contains "dog"
- `front:` - empty field
- `fr*:text` - fields starting with "fr"

## Tags, Decks, and Cards

- `tag:animal` - includes subtags
- `deck:french` - top-level deck and subdecks
- `card:forward` - by card type name
- `note:basic` - by note type

## Card State and Properties

- `is:due`, `is:new`, `is:learn`, `is:review`, `is:suspended`, `is:buried`
- `prop:ivl>=10` - interval-based searches
- `prop:due=1` - cards due tomorrow
- `flag:1` through `flag:7` - flag colors

## Recent Events

- `added:7` - last 7 days
- `rated:1:2` - answered "Hard" today
- `introduced:365` - first answered within last year

## Advanced Features

- **Regular expressions**: `re:(some|another).*thing`
- **Combining characters**: `nc:uber` matches "über"
- **Custom data**: `has-cd:v` or `prop:cdn:d>5`

Special characters like `*`, `_`, and `"` require escaping with backslashes or quotes.
