# Card Info, Graphs and Statistics

## Card Info

Access card information via Cards > Info menu, right-click selection, or pressing I during study sessions.

**Position**
Indicates the card's order among new cards; changeable in the browser but unused after initial study unless manually reset.

**Interval**
The spacing between reviews, abbreviated as "0s, 1m, 3h, 4d, 5mo, 6y" for seconds, minutes, hours, days, months, and years.

**Ease**
Represents how much the interval expands when answering "Good" on review cards.

The review history section displays past card activity, with ratings indicating button choices (1 = Again, 4 = Easy). Manually rescheduled cards show "Manual" type with 0 rating.

## Statistics

Access via the Stats button or T key from the main window.

### Selecting Decks / Collection

**Deck**
By default shows statistics for the current deck and subdecks. Type a deck name or use the deck selector to view different decks.

**Collection**
Check this option to display statistics across your entire collection or add search filters for specific queries.

**History**
Change the time scope from the last 12 months to all history or deck life scope. The "today" section remains unaffected.

**More**
- Save statistics as PDF for sharing
- Deleted note review histories persist in collection-wide statistics
- Shift-click the Stats button to access older graph designs (Anki 2.1.28+)

## Today

A textual summary of completed reviews. "A review" equals one card answer, so cards studied multiple times count as multiple reviews.

**Again Count**
Number of failed reviews (Again button presses); the correct percentage shows non-failed cards divided by total studied.

**Learn, Review, Relearn, Filtered**
Categorizes reviews by card type or filtered deck study.

These daily statistics lack predictive value for learning progress; longer-term data provides better insight.

## The Graphs

**Future Due**
Projects estimated review volume on future days assuming no new learning or failures. Bars show daily study volume; gray regions show dormant scenario volume. Daily load calculates average daily reviews using the formula: ∑(1/Interval) for each card.

**Calendar**
Displays historical review activity; hover for daily totals, click day names to adjust weekly starting point.

**Reviews**
Counts card reviews by time period, color-coded by card maturity (mature, young, relearning, learning). Gray shading shows cumulative totals.

**Card Counts**
Pie chart showing deck/collection composition by card status (mature, unseen, young/learn, suspended) with exact counts.

**Review Time**
Mirrors Review Count but measures time spent rather than quantity answered.

**Review Intervals**
Shows card distribution across interval lengths; gray regions indicate percentage of cards at or below each threshold.

**Card Ease**
Displays ease factor distribution with average ease for selected scope.

**Card Stability** (FSRS only)
Time required for recall probability to decrease from 100% to 90%.

**Card Difficulty** (FSRS only)
Determines interval growth rate following reviews.

**Card Retrievability** (FSRS only)
Probability of recall; estimated total knowledge multiplies average retrievability by reviewed cards.

**Hourly Breakdown**
Charts review success percentage by hour of day, with blue bars indicating review volume and gray regions showing pass percentages.

**Answer Buttons**
Shows frequency of Again, Hard, Good, and Easy button usage across card types with correct answer percentages.

**True Retention Table**
Retention data across cards and timeframes (mature cards = interval ≥21 days). One review daily counts; Hard/Good/Easy = pass, Again = fail. FSRS users should match true retention to desired retention settings.

## Manual Analysis

Advanced users can access raw data through add-ons or direct database querying. Anki uses SQLite format; tools like SQLite Browser enable exploration.

The **revlog table** stores individual review entries with these columns:

- **id**: Unix epoch milliseconds of review
- **cid**: Card ID (links to cards table)
- **usn**: Sync tracking (non-analytical)
- **ease**: Button pressed (1=Again, 4=Easy)
- **ivl**: New interval (positive=days, negative=seconds for learning)
- **lastIvl**: Prior interval before review
- **factor**: New ease in permille (2500 = 2.5x multiplier)
- **time**: Milliseconds spent on question and answer
- **type**: 0=learning, 1=review, 2=relearning, 3=cram cards
