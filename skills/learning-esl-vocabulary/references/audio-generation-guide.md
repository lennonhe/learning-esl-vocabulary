# Audio Generation Guide

This guide explains how to generate audio files for vocabulary reviews.

## Overview

Audio generation is **optional**. The skill works perfectly without it, but audio helps with pronunciation practice and listening comprehension.

Two audio speeds are generated for each review:
- **Slow** (90% speed): For careful listening and pronunciation practice
- **Normal** (100% speed): For natural listening practice

## Prerequisites

Choose one audio engine:

### Option 1: OpenAI TTS (Recommended)
- **Pros**: High-quality voices, natural-sounding speech
- **Cons**: Requires API key and incurs costs
- **Setup**:
  1. Install packages: `pip install openai imageio-ffmpeg`
  2. Set environment variable: `OPENAI_API_KEY=your_api_key`

### Option 2: edge-tts (Free Alternative)
- **Pros**: Free, no API key needed, good quality
- **Cons**: Requires internet connection, voices less natural than OpenAI
- **Setup**: `pip install edge-tts`

## How It Works

The skill automatically detects which engine is available:

1. **First**, checks if `OPENAI_API_KEY` is set → uses OpenAI TTS
2. **Otherwise**, checks if `edge-tts` is installed → uses edge-tts
3. **If neither**, skips audio generation and informs the user

## Usage

### For Daily Reviews

When you run `review`, the skill generates:
- `YYYY-MM-DD/daily-review-slow.mp3`
- `YYYY-MM-DD/daily-review-normal.mp3`

**OpenAI TTS command**:
```bash
python scripts/openai-tts.py "TEXT" "{target-date}/daily-review-slow.mp3" slow
python scripts/openai-tts.py "TEXT" "{target-date}/daily-review-normal.mp3" normal
```

**edge-tts command**:
```bash
python scripts/edge-tts-wrapper.py "TEXT" "{target-date}/daily-review-slow.mp3" slow
python scripts/edge-tts-wrapper.py "TEXT" "{target-date}/daily-review-normal.mp3" normal
```

### For PDF Imports

When you run `import-review`, the skill generates:
- `bbdc-review/YYYY-MM-DD/{pdf-basename}-review-slow.mp3`
- `bbdc-review/YYYY-MM-DD/{pdf-basename}-review-normal.mp3`

**Process**:
1. Combine all paragraphs with "Paragraph 1. ... Paragraph 2. ..." format
2. Write combined text to: `bbdc-review/{date}/{pdf-basename}-audio-text.txt`
3. Generate audio using OpenAI TTS or edge-tts (same commands as daily review, with `--file` flag)
4. Delete the temporary text file after generation

**OpenAI TTS command**:
```bash
python scripts/openai-tts.py --file "bbdc-review/{date}/{pdf-basename}-audio-text.txt" "bbdc-review/{date}/{pdf-basename}-review-slow.mp3" slow
python scripts/openai-tts.py --file "bbdc-review/{date}/{pdf-basename}-audio-text.txt" "bbdc-review/{date}/{pdf-basename}-review-normal.mp3" normal
```

**edge-tts command**:
```bash
python scripts/edge-tts-wrapper.py --file "bbdc-review/{date}/{pdf-basename}-audio-text.txt" "bbdc-review/{date}/{pdf-basename}-review-slow.mp3" slow
python scripts/edge-tts-wrapper.py --file "bbdc-review/{date}/{pdf-basename}-audio-text.txt" "bbdc-review/{date}/{pdf-basename}-review-normal.mp3" normal
```

## Troubleshooting

### "Audio generation skipped" message

This means neither OpenAI TTS nor edge-tts is configured. To fix:

1. **For OpenAI TTS**:
   - Install: `pip install openai imageio-ffmpeg`
   - Set API key: `export OPENAI_API_KEY=your_key` (Unix/macOS) or `set OPENAI_API_KEY=your_key` (Windows)

2. **For edge-tts**:
   - Install: `pip install edge-tts`

### OpenAI TTS errors

- **"Invalid API key"**: Check that `OPENAI_API_KEY` is set correctly
- **"Token limit exceeded"**: Text is too long. The scripts automatically chunk text for OpenAI's token limits.

### edge-tts errors

- **"No connection"**: Check internet connection
- **Import error**: Reinstall with `pip install --upgrade edge-tts`

## Configuration

For OpenAI TTS, you can customize the voice and model in `references/config.json`:

```json
{
  "tts": {
    "openai": {
      "model": "gpt-4o-mini-tts",
      "voice": "alloy",
      "slow_instructions": "Speak clearly and naturally, at a slightly slower than normal pace...",
      "normal_instructions": "Speak naturally at a slightly faster than normal pace..."
    }
  }
}
```

Available voices: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`

For edge-tts, voices are configured in the wrapper script (default: `en-US-JennyNeural`).
