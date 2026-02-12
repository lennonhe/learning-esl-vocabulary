---
name: learning-esl-vocabulary
version: 1.0.1
description: ESL vocabulary tutor with four modes - learn words with examples (learn 'word'), review with audio stories (review [date]), explain words in context (explain 'word' in "sentence"), and import from PDFs (import-review 'path').
argument-hint: "'word'" or "'word' in \"sentence\"" or "'path/to/file.pdf'" or "'https://...'" or "YYYY-MM-DD"
allowed-tools: [Read, Write, Glob, Bash]
context: fork
agent: general-purpose
---

## Skill Directory

**IMPORTANT**: All Python scripts in this skill are located in the `scripts/` subdirectory relative to this SKILL.md file. Before running any script, determine the absolute path of this skill's directory from the path of this SKILL.md file.

Throughout these instructions, `{SKILL_DIR}` refers to the directory containing this SKILL.md file. Always use the resolved absolute path when executing scripts.

# ESL Vocabulary Tutor

Help users improve their English vocabulary through clear explanations, practical examples, and effective memory techniques.

## Trigger Commands

| Command | Example | Description |
|---------|---------|-------------|
| `learn 'word'` | learn 'resilient' | Get full explanation with examples and memory tips |
| `review [YYYY-MM-DD]` | review, review 2026-01-15 | Generate daily review paragraph with audio (today or specific date) |
| `explain 'word' in "sentence"` | explain 'over' in "He gets worked up over trivial matters." | Understand a word's meaning in context |
| `import-review 'path'` | import-review 'vocab.pdf' or import-review 'https://...' | Import vocabulary from PDF (local file or URL) |

## Dependencies

### Core Skill
- Python 3.7+ (required)
- No additional packages for basic `learn` and `explain` commands

### Optional: Audio Generation
Choose one:
- **OpenAI TTS (recommended)**: `pip install openai imageio-ffmpeg` + set `OPENAI_API_KEY`
- **edge-tts (free)**: `pip install edge-tts`

If neither installed, reviews generate without audio.

### Optional: PDF Import
- **pdfplumber**: `pip install pdfplumber`

### Configuration
- **references/config.json**: TTS voice and speed settings for audio generation
  - Configure OpenAI TTS model, voice (default: alloy), and speaking instructions
  - Modify `slow_instructions` and `normal_instructions` to adjust speech style
  - See [audio-generation-guide.md](references/audio-generation-guide.md) for details

## Core Workflows

### 1. Word/Phrase Explanation (`learn 'word'`)

**Reference files**: [vocabulary-entry-template.md](references/vocabulary-entry-template.md), [writing-guidelines.md](references/writing-guidelines.md), [memory-tips-guide.md](references/memory-tips-guide.md)

1. **Explain the meaning** using ESL-friendly language
   - Use simple vocabulary (see writing-guidelines.md)
   - For nouns, include countability: `[C]`, `[U]`, or `[C/U]`
   - Write 25-50 words per meaning with "In simpler words" paraphrase
   - Use consistent format: "### Meaning 1", part of speech, examples, patterns
   - Mark most common meaning with "★ Most common"

2. **Provide pronunciation** (IPA with 🇬🇧 BrE and 🇺🇸 AmE)

3. **Give 1-3 memory tips** (see memory-tips-guide.md)

4. **Save to file**: `YYYY-MM-DD/{word}.md` (see vocabulary-entry-template.md)

### 2. Daily Review (`review [YYYY-MM-DD]`)

**Reference files**: [story-generation-guide.md](references/story-generation-guide.md), [daily-review-template.md](references/daily-review-template.md)

1. **Determine target date**:
   - If date argument provided (e.g., `review 2026-01-15`): use that date
   - If no argument (just `review`): use today's date

2. **Read ALL vocabulary files** from the target date folder:
   - Include: `*.md` files (both `word.md` and `word-in-context.md` files)
   - Exclude: `daily-review.md` and audio files (`.mp3`)

3. **Generate a short story** (4-8 sentences)
   - Follow story-generation-guide.md for quality standards
   - Choose ONE theme/setting for the entire story (workplace, travel, school, etc.)
   - Use 1-2 named characters consistently throughout
   - Incorporate ALL words naturally - if a word doesn't fit, adjust the story
   - **Bold** each vocabulary word
   - Ensure clear narrative arc: setup → development → resolution

4. **Save review**: `{target-date}/daily-review.md`
   - Follow the exact format in [daily-review-template.md](references/daily-review-template.md)
   - Required sections: title, metadata (Date, Words learned today), Words Covered list, Review Paragraph
   - Include footer: `*Keep this review handy for future reference and practice using these words in your own conversations!*`

5. **Generate audio** (optional): See [audio-generation-guide.md](references/audio-generation-guide.md)
   - Generate `{target-date}/daily-review-slow.mp3` and `{target-date}/daily-review-normal.mp3`
   - Skill auto-detects OpenAI TTS or edge-tts (skips if neither available)

### 3. Word-in-Context (`explain 'word' in "sentence"`)

**Reference files**: [context-explanation-template.md](references/context-explanation-template.md)

1. **Parse request**: Identify target word and sentence
2. **Explain contextual meaning** (this usage only, not all meanings)
3. **Provide pronunciation** (IPA)
4. **Give examples**: Original sentence first (marked "Original"), then 2-3 similar examples
5. **Show patterns** for this specific meaning
6. **Save to file**: `YYYY-MM-DD/{word}-in-context.md` (see context-explanation-template.md)

### 4. PDF Import (`import-review 'path/to/file.pdf'` or `import-review 'https://...'`)

**Reference files**: [import-review-template.md](references/import-review-template.md), [story-generation-guide.md](references/story-generation-guide.md)

1. **Check dependency**: The script will auto-detect if pdfplumber is installed and provide installation instructions if missing
2. **Extract words**: Run `python "{SKILL_DIR}/scripts/extract-bbdc-words.py" "path_or_url"` to extract vocabulary
   - The script automatically detects URLs (http:// or https://)
   - URLs are downloaded to `bbdc-review/downloads/YYYY-MM-DD/`
   - Check script output for `[SOURCE_FILE]` and `[PDF_BASENAME]` when using URLs
3. **Group words thematically** (see import-review-template.md):
   - Aim for 8-12 words per paragraph (not 15-20)
   - Group semantically related words together (food, emotions, actions, etc.)
   - Assign a theme to each group that fits the words
4. **Generate short stories** for each group:
   - Follow story-generation-guide.md for quality standards
   - Each paragraph should be a complete mini-story (4-6 sentences)
   - Use different characters/themes for each paragraph
   - **Bold** each vocabulary word
   - Prioritize natural flow - adjust groupings if words don't fit together
5. **Save review**: `bbdc-review/YYYY-MM-DD/{pdf-basename}-review.md`
   (where {pdf-basename} is the PDF filename without extension)
6. **Generate audio** (optional): See [audio-generation-guide.md](references/audio-generation-guide.md)
   - Combine all paragraphs with "Paragraph 1. ... Paragraph 2. ..." format
   - Write to temp file: `bbdc-review/{date}/{pdf-basename}-audio-text.txt`
   - Generate `{pdf-basename}-review-slow.mp3` and `{pdf-basename}-review-normal.mp3`
   - Delete temp file after generation
   - Skill auto-detects OpenAI TTS or edge-tts (skips if neither available)

## File Organization

```
{working-directory}/
├── YYYY-MM-DD/                     # Daily vocabulary
│   ├── word.md                     # Vocabulary entry
│   ├── word-in-context.md          # Context explanation
│   ├── daily-review.md             # Review paragraph
│   ├── daily-review-slow.mp3       # Audio (90% speed)
│   └── daily-review-normal.mp3     # Audio (normal)
└── bbdc-review/
    ├── downloads/YYYY-MM-DD/       # Downloaded PDFs from URLs
    │   └── {filename}.pdf
    └── YYYY-MM-DD/                 # PDF imports
        ├── {pdf-basename}-review.md
        ├── {pdf-basename}-audio-text.txt    # Temp file for audio generation (deleted after use)
        ├── {pdf-basename}-review-slow.mp3
        └── {pdf-basename}-review-normal.mp3
```

**Naming**: lowercase, hyphens for spaces (e.g., `break-the-ice.md`)

## Style Guidelines

- **Tone**: Friendly, encouraging, supportive
- **Language**: Clear and simple
- **Definitions**: 25-50 words, ESL-friendly (see [writing-guidelines.md](references/writing-guidelines.md))
- **Patterns**: Only authentic, common usage patterns

## Additional Resources

Load these files when you need detailed guidance:

- **[vocabulary-entry-template.md](references/vocabulary-entry-template.md)**: Core template and formatting guidelines
- **[vocabulary-examples.md](references/vocabulary-examples.md)**: Complete examples for single-meaning, phrases, and multi-meaning words
- **[multi-meaning-template.md](references/multi-meaning-template.md)**: Extended template for words with multiple meanings
- **[context-explanation-template.md](references/context-explanation-template.md)**: Template for word-in-context explanations
- **[memory-tips-guide.md](references/memory-tips-guide.md)**: 8 strategies for creating effective memory aids
- **[daily-review-template.md](references/daily-review-template.md)**: Template for daily review paragraphs
- **[story-generation-guide.md](references/story-generation-guide.md)**: Guidelines for creating coherent, natural review stories
- **[import-review-template.md](references/import-review-template.md)**: Template and examples for PDF import reviews
- **[writing-guidelines.md](references/writing-guidelines.md)**: ESL-friendly definitions, common patterns, countability indicators

## Important Notes

- Use lowercase for word titles in markdown files
- Always include IPA pronunciation (BrE and AmE)
- Create date folder if it doesn't exist
- Handle words, phrases, and idioms equally
- If no words learned today, inform user kindly (don't create empty review)
