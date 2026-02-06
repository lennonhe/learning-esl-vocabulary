# PDF Import Review Template

Template for generating review paragraphs from imported PDF vocabulary lists.

## Output Files

Files are saved to `bbdc-review/YYYY-MM-DD/` using the PDF filename as a base:
- `{pdf-basename}-review.md` - Review document
- `{pdf-basename}-review-slow.mp3` - Audio at 90% speed (optional)
- `{pdf-basename}-review-normal.mp3` - Audio at normal speed (optional)

Example: For `bbdc_30870577_20260130143429.pdf`:
- `bbdc_30870577_20260130143429-review.md`
- `bbdc_30870577_20260130143429-review-slow.mp3`
- `bbdc_30870577_20260130143429-review-normal.mp3`

## File Structure

```markdown
# PDF Vocabulary Review

**Date**: {YYYY-MM-DD}
**Source**: {filename.pdf}
**Total words**: {count}

## Paragraph 1: {Theme}

**Words**: word1, word2, word3, word4, word5, word6, word7, word8

{4-6 sentence story incorporating all words naturally}

## Paragraph 2: {Theme}

**Words**: word9, word10, word11, word12, word13, word14, word15, word16

{4-6 sentence story incorporating all words naturally}

[Continue for remaining word groups...]

---

*Review generated from PDF import. Practice reading aloud for pronunciation!*
```

## Grouping Strategy

### Step 1: Sort words by semantic category

Before writing, categorize all extracted words:

| Category | Example words |
|----------|---------------|
| Food/Cooking | lasagne, spinach, appetite, simmer |
| Movement/Action | stomp, dash, leap, stroll |
| Emotions | anxious, delighted, frustrated, serene |
| Work/Business | negotiate, deadline, collaborate, promote |
| Nature | meadow, breeze, blossom, creek |
| Relationships | companion, acquaintance, bond, estranged |

### Step 2: Create groups of 8-12 words

- Prioritize semantic similarity within each group
- If categories are too small, combine related categories
- Aim for words that can naturally appear in the same story

### Step 3: Assign a theme to each group

Match the theme to the dominant word category:
- Food words → cooking/restaurant/family dinner theme
- Movement words → sports/adventure/travel theme
- Emotion words → personal story/relationship theme

## Example: Well-Structured Import Review

# PDF Vocabulary Review

**Date**: 2026-01-30
**Source**: bbdc-vocabulary.pdf
**Total words**: 24

## Paragraph 1: Kitchen Adventure

**Words**: lasagne, spinach, appetite, simmer, aroma, portion, savor, ingredient

Maria had been looking forward to cooking **lasagne** for her family all week. She carefully prepared each **ingredient**, including fresh **spinach** from the garden. As the dish began to **simmer** in the oven, a wonderful **aroma** filled the kitchen. Her children came running, their **appetite** growing with every passing minute. When dinner was finally ready, Maria served generous **portions** to everyone. The family took their time to **savor** each delicious bite, complimenting the chef on her masterpiece.

## Paragraph 2: Morning Commute

**Words**: dash, stroll, pedestrian, intersection, commute, punctual, detour, congestion

Every morning, Tom faces the challenge of his **commute** to work. He prefers to **stroll** through the park when time allows, enjoying the peaceful scenery. However, today he had to **dash** out of his apartment after oversleeping. At the busy **intersection** near his office, he noticed heavy **congestion** blocking the usual route. A helpful **pedestrian** suggested taking a **detour** through the side streets. Thanks to this advice, Tom still managed to be **punctual** for his important meeting.

## Paragraph 3: Weekend Emotions

**Words**: anxious, delighted, frustrated, relieved, anticipate, overwhelmed, grateful, composed

Jenny felt **anxious** as she waited for her exam results to be posted online. She had studied hard but couldn't help feeling **overwhelmed** by the pressure. When the website finally loaded, she was **delighted** to see she had passed with excellent marks. All the **frustration** from those long study nights suddenly felt worthwhile. She called her parents, who had been **anticipating** the news just as eagerly. Feeling **relieved** and **grateful** for their support, Jenny remained **composed** as she thanked them for believing in her.

---

*Review generated from PDF import. Practice reading aloud for pronunciation!*

## Quality Standards

Each paragraph must:

1. **Tell a complete mini-story** (beginning, middle, end)
2. **Use a consistent character** (1-2 per paragraph)
3. **Stay in one setting** (don't jump locations)
4. **Integrate words naturally** (not forced)
5. **Be 4-6 sentences** (not too short, not too long)

## Common Mistakes to Avoid

### Mistake 1: Too many words per paragraph
❌ 15-20 words → sentences become awkward
✓ 8-12 words → natural integration possible

### Mistake 2: Random word grouping
❌ Grouping by position in PDF
✓ Grouping by semantic similarity

### Mistake 3: No story structure
❌ "He was anxious. She felt delighted. They were frustrated."
✓ Connected narrative with cause and effect

### Mistake 4: Forcing unrelated words together
❌ "She ate lasagne while feeling anxious about the intersection."
✓ Separate paragraphs for food words and commute words
