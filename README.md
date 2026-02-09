# Learning ESL Vocabulary - Claude Code Plugin

A powerful Claude Code plugin that helps ESL learners improve their English vocabulary through clear explanations, practical examples, and effective memory techniques.

## Features

- **Word/Phrase Explanations**: Get clear definitions, 2-4 example sentences, and 1-3 memory tips for any English word, phrase, or idiom
- **Common Patterns**: Each vocabulary entry includes common usage patterns (collocations, sentence structures) to help you use words naturally
- **Automatic File Organization**: Vocabulary entries are automatically saved in date-organized folders (YYYY-MM-DD format)
- **Daily Reviews**: Generate cohesive paragraphs that naturally incorporate all words learned in a day
- **Audio Support**: Daily reviews can be generated as MP3 audio files with slow and normal speed versions for listening practice
- **Smart Chunking**: Automatically handles long text (>1500 characters) by splitting at sentence boundaries and seamlessly concatenating audio
- **ESL-Friendly**: Clear, simple language suitable for English language learners

## Installation

### Via Marketplace (Recommended)

```bash
# Add Lennon's plugin marketplace
claude plugin marketplace add LennonHe/lennon-claude-code-plugins

# Install this plugin
claude plugin install learning-esl-vocabulary@lennon-claude-code-plugins
```

### Direct Installation

```bash
# Install directly from GitHub
claude plugin install https://github.com/LennonHe/learning-esl-vocabulary.git
```

## Usage

### Learning a New Word

Use the `learn` command to learn a word, phrase, or idiom:

```
learn 'resilient'
learn 'break the ice'
learn 'piece of cake'
```

Claude will:
- Explain the meaning in clear, simple English
- Provide 2-4 example sentences showing typical usage
- Include common patterns to remember (collocations, sentence structures)
- Give 1-3 memory tips to help you remember
- Save the entry to a markdown file in today's date folder

### Daily Review

At the end of the day, request a vocabulary review:

```
review
```

Claude will:
- Read all vocabulary entries from today
- Generate a cohesive paragraph using all the words
- Save the review as `daily-review.md` in today's folder
- Generate audio files (if TTS is configured):
  - `daily-review-slow.mp3` - 90% speed for clear listening
  - `daily-review-normal.mp3` - Normal speed for practice

### Word-in-Context Explanation

When you encounter a word in a sentence and want to understand its specific meaning:

```
explain 'over' in "He gets worked up over trivial matters."
explain 'run' in "She runs a successful business."
```

Claude will:
- Explain the specific meaning of the word in that context
- Provide additional example sentences with the same meaning
- Show common patterns for this particular usage
- Save the entry as `{word}-in-context.md` in today's folder

## Audio Setup (Optional)

The plugin supports OpenAI TTS for audio generation with automatic chunking for long text.

### OpenAI TTS Setup

OpenAI TTS provides high-quality, natural-sounding voices with support for long text through automatic chunking.

1. **Install required packages:**
   ```bash
   pip install openai imageio-ffmpeg
   ```

   - `openai`: OpenAI Python client for TTS API
   - `imageio-ffmpeg`: Bundled ffmpeg for audio concatenation (no system installation needed)

2. **Set your API key as an environment variable:**

   **Windows (PowerShell):**
   ```powershell
   $env:OPENAI_API_KEY='sk-your-actual-api-key'
   ```

   **macOS/Linux (Bash):**
   ```bash
   export OPENAI_API_KEY='sk-your-actual-api-key'
   ```

3. **Create or edit the config file:**

   Create `config.json` in the `skills/learning-esl-vocabulary/references/` directory:
   ```json
   {
     "tts": {
       "provider": "openai",
       "openai": {
         "model": "gpt-4o-mini-tts",
         "voice": "alloy",
         "slow_instructions": "Speak clearly and naturally, at a slightly slower than normal pace, with warm tone, gentle pauses between sentences, and careful articulation. This audio is for English learners, so prioritize clarity and smooth flow without sounding robotic.",
         "normal_instructions": "Speak naturally at a slightly faster than normal pace, with smooth linking, natural reductions, and conversational rhythm, while remaining clear and intelligible for advanced English learners."
       }
     }
   }
   ```

**Available voices**: alloy, ash, ballad, coral, echo, fable, nova, onyx, sage, shimmer

**Custom API base URL**: Set the `OPENAI_BASE_URL` environment variable if using a compatible API provider (like Azure OpenAI):
```bash
export OPENAI_BASE_URL='https://your-api-endpoint.com/v1'
```

**Long Text Support**: The plugin automatically handles long text (>1500 characters) by:
- Splitting text at sentence boundaries for natural transitions
- Generating audio for each chunk separately
- Seamlessly concatenating chunks using ffmpeg
- No manual intervention needed - works transparently

### Alternative: edge-tts (Free Fallback)

If OpenAI TTS is not configured, the plugin can fall back to edge-tts:

```bash
pip install edge-tts
```

Note: edge-tts does not support the same level of customization or chunking features.

## File Organization

The plugin automatically organizes your vocabulary files:

```
your-working-directory/
└── 2026-01-28/
    ├── resilient.md
    ├── break-the-ice.md
    ├── ambitious.md
    ├── daily-review.md
    ├── daily-review-slow.mp3      # Audio at 90% speed
    └── daily-review-normal.mp3    # Audio at normal speed
```

## Dependencies

- Python 3.7+ (for audio generation scripts)
- Optional: `pip install openai imageio-ffmpeg` (for TTS support)
- Optional: `pip install edge-tts` (free TTS fallback)

## Tips for Best Results

1. **Use simple commands**: `learn 'word'`, `review`, or `explain 'word' in "sentence"`
2. **Review regularly**: Use the daily review feature to reinforce learning
3. **Explore your files**: Browse the date folders to see your vocabulary progress over time
4. **Practice**: Try using the words from your daily review in your own sentences

## Example Interaction

**You**: learn 'resilient'

**Claude**: I'll help you learn "resilient"!

**Meaning**: Resilient means able to recover quickly from difficulties or challenges...

[Full explanation with examples and memory tips]

I've saved this to 2026-01-28/resilient.md for your reference!

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

This plugin was created following Anthropic's plugin creation best practices. If you encounter any issues or have suggestions for improvement, please [open an issue](https://github.com/LennonHe/learning-esl-vocabulary/issues).
