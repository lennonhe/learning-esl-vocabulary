# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code plugin that helps ESL learners improve their English vocabulary through four modes: learning new words with examples, generating daily reviews with audio, explaining words in context, and importing vocabulary from PDFs.

**Plugin Type**: Agent skill with progressive disclosure architecture
**Version**: 1.0.1
**Distribution**: Via plugin marketplace (LennonHe/lennon-claude-code-plugins)

## Architecture

### Plugin Structure

```
.claude-plugin/
  plugin.json           # Plugin manifest (name, version, description)
skills/
  learning-esl-vocabulary/
    SKILL.md            # Main skill definition with workflows
    scripts/            # Python automation scripts
      openai-tts.py     # OpenAI TTS with chunking support
      edge-tts-wrapper.py
      extract-bbdc-words.py
    references/         # Template and guide files
      config.json       # TTS configuration
      *.md              # Templates and guidelines
```

### Progressive Disclosure Pattern

This skill follows Anthropic's progressive disclosure architecture:

1. **SKILL.md** contains core workflows and references to detailed guides
2. **references/** directory contains specialized templates and guidelines that are loaded only when needed
3. References are linked with markdown relative paths: `[template](references/template.md)`

When modifying the skill:
- Keep SKILL.md under 500 lines (currently ~189 lines)
- Put detailed instructions in `references/` files
- Update cross-references when adding new template files

### Script Path Resolution

All Python scripts use relative paths from SKILL.md location. The skill uses `{SKILL_DIR}` placeholder pattern:

1. Determine the absolute path of the skill directory from SKILL.md location
2. Resolve script paths: `"{SKILL_DIR}/scripts/openai-tts.py"`
3. Always use double quotes around paths (Windows compatibility)

Example:
```bash
# If SKILL.md is at: D:/path/to/skills/learning-esl-vocabulary/SKILL.md
# Then SKILL_DIR is: D:/path/to/skills/learning-esl-vocabulary
python "{SKILL_DIR}/scripts/openai-tts.py" "text" "output.mp3"
```

## Testing the Plugin

### Local Testing

Use `--plugin-dir` flag to test during development:

```bash
claude --plugin-dir .
```

This loads the plugin without installing it. Test each workflow:
- Try `learn 'word'` command
- Test `review` with existing date folders
- Verify `explain 'word' in "sentence"` format
- Check `import-review` with sample PDF

### Creating Test Data

Create a test date folder with sample vocabulary files:

```bash
mkdir 2026-02-12
# Add sample word files to test daily review generation
```

## Key Components

### TTS Audio Generation

Two Python scripts handle text-to-speech:

1. **openai-tts.py** (recommended):
   - Automatic chunking for long text (>1500 chars)
   - Sentence-boundary splitting for natural transitions
   - Uses `imageio-ffmpeg` for audio concatenation
   - Reads config from `references/config.json`
   - Modes: "slow" (with `slow_instructions`) or "normal" (with `normal_instructions`)

2. **edge-tts-wrapper.py** (free fallback):
   - No chunking support
   - Simpler implementation

Both scripts:
- Accept text via argument or `--file` flag
- Output MP3 files
- Return exit codes (0 = success, non-zero = error)

### PDF Import

**extract-bbdc-words.py**:
- Extracts vocabulary from PDFs (local files or URLs)
- Auto-detects URLs (http:// or https://)
- Downloads URLs to `bbdc-review/downloads/YYYY-MM-DD/`
- Outputs extracted words for processing
- Requires `pdfplumber` package

### Configuration

**references/config.json**:
```json
{
  "tts": {
    "provider": "openai",
    "openai": {
      "model": "gpt-4o-mini-tts",
      "voice": "alloy",
      "slow_instructions": "...",
      "normal_instructions": "..."
    }
  }
}
```

Environment variables:
- `OPENAI_API_KEY` (required for OpenAI TTS)
- `OPENAI_BASE_URL` (optional, for custom endpoints)

## Content Generation Guidelines

### ESL-Friendly Language

All generated content must use simple, clear language suitable for English learners:

- **Definitions**: 25-50 words per meaning
- **Structure**: "In simpler words" paraphrase after main definition
- **Vocabulary**: Avoid complex or advanced words in definitions
- See `references/writing-guidelines.md` for detailed rules

### Story Generation

Daily reviews and PDF imports use short story format:

- **Length**: 4-8 sentences for daily reviews, 4-6 for PDF paragraphs
- **Structure**: Setup → development → resolution
- **Characters**: 1-2 named characters used consistently
- **Theme**: Single theme per story (workplace, travel, school, etc.)
- **Word integration**: ALL vocabulary words must appear naturally (bold each word)
- See `references/story-generation-guide.md` for quality standards

### Template System

Each workflow has a corresponding template:

| Workflow | Template File | Purpose |
|----------|---------------|---------|
| `learn` | vocabulary-entry-template.md | Standard word entries |
| `learn` (multi-meaning) | multi-meaning-template.md | Words with 2+ meanings |
| `review` | daily-review-template.md | Daily review format |
| `explain` | context-explanation-template.md | Context-specific meanings |
| `import-review` | import-review-template.md | PDF import reviews |

When modifying templates:
- Maintain consistent markdown formatting
- Keep section headers exact (used for parsing)
- Update corresponding examples in `references/vocabulary-examples.md`

## Modifying the Skill

### Updating SKILL.md

When adding new features or workflows:

1. Update the trigger commands table
2. Add workflow section with reference links
3. Keep core instructions concise (delegate details to references/)
4. Update version in YAML frontmatter
5. Update `.claude-plugin/plugin.json` version

### Adding Reference Files

To add new templates or guides:

1. Create file in `skills/learning-esl-vocabulary/references/`
2. Add link in SKILL.md's "Additional Resources" section
3. Use relative markdown links: `[name](references/filename.md)`
4. Keep references one level deep (no nested references)

### Modifying Python Scripts

Scripts are standalone utilities:
- Use absolute paths for file operations
- Accept command-line arguments for flexibility
- Return meaningful exit codes
- Print helpful error messages to stderr
- Don't require modification of SKILL.md when changing implementation details

## File Organization Patterns

### Daily Vocabulary

```
{working-directory}/
  YYYY-MM-DD/
    word.md                    # Standard vocabulary entry
    word-in-context.md         # Context-specific explanation
    daily-review.md            # Generated review paragraph
    daily-review-slow.mp3      # Audio at 90% speed
    daily-review-normal.mp3    # Audio at normal speed
```

### PDF Imports

```
{working-directory}/
  bbdc-review/
    downloads/YYYY-MM-DD/
      filename.pdf             # Downloaded PDFs from URLs
    YYYY-MM-DD/
      pdf-basename-review.md
      pdf-basename-review-slow.mp3
      pdf-basename-review-normal.mp3
```

### Naming Conventions

- Use lowercase for all file names
- Replace spaces with hyphens: `break-the-ice.md`
- Date format: `YYYY-MM-DD`
- Context explanations: `{word}-in-context.md`
- PDF reviews: `{pdf-basename}-review.md`

## Common Development Tasks

### Testing TTS Integration

```bash
# Test OpenAI TTS directly
cd skills/learning-esl-vocabulary
python scripts/openai-tts.py "Test sentence." "test-output.mp3" slow

# Test with config.json
python scripts/openai-tts.py --file test-input.txt test-output.mp3 normal
```

### Testing PDF Extraction

```bash
cd skills/learning-esl-vocabulary
python scripts/extract-bbdc-words.py "path/to/test.pdf"
python scripts/extract-bbdc-words.py "https://example.com/test.pdf"
```

### Validating Templates

When modifying templates, create test vocabulary entries and verify:
- Markdown rendering (preview in markdown viewer)
- Section header consistency
- Example sentence formatting
- Bold vocabulary words in stories

## Best Practices Compliance

This plugin follows Anthropic's agent skill best practices:

- ✓ Concise SKILL.md (<500 lines)
- ✓ Progressive disclosure with reference files
- ✓ Third-person descriptions in frontmatter
- ✓ Specific trigger terms in description
- ✓ Utility scripts for fragile operations
- ✓ One-level-deep file references
- ✓ Forward slashes in all paths (cross-platform)
- ✓ Semantic versioning

When making changes, maintain these patterns to ensure compatibility with Claude Code's skill system.

## Distribution

This plugin is distributed via plugin marketplace:

```bash
# Installation command for users
claude plugin install learning-esl-vocabulary@lennon-claude-code-plugins
```

When releasing updates:
1. Update version in both `.claude-plugin/plugin.json` and SKILL.md
2. Use semantic versioning (MAJOR.MINOR.PATCH)
3. Test with `--plugin-dir` flag before committing
4. Update README.md with new features
5. Commit and push to trigger marketplace update
