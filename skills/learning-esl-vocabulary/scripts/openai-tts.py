#!/usr/bin/env python3
"""
OpenAI TTS helper script for the Learning ESL Vocabulary skill.
Generates audio files using OpenAI's text-to-speech API.

Features:
    - Automatic chunking for long text (>1500 chars) to handle 2000 token limit
    - Sentence-boundary splitting for natural audio transitions
    - Seamless concatenation using ffmpeg

Usage:
    python openai-tts.py "text to speak" "output.mp3" [mode]
    python openai-tts.py --file "input.txt" "output.mp3" [mode]

Arguments:
    text: The text to convert to speech (or --file flag for file input)
    output: Output filename (MP3)
    mode: Optional speed mode - "slow" or "normal" (reads instructions from config.json)

Configuration:
    - OPENAI_API_KEY: Environment variable (required)
    - OPENAI_BASE_URL: Environment variable (optional, defaults to https://api.openai.com/v1)
    - config.json: TTS settings (model, voice, instructions)

Dependencies:
    - openai: OpenAI Python client (pip install openai)
    - imageio-ffmpeg: Bundled ffmpeg for audio concatenation (pip install imageio-ffmpeg)
"""

import sys
import json
import os
from pathlib import Path

# Constants - conservative limit for 2000 token limit
# English: ~0.75 tokens per character, so 1500 chars ≈ 1125 tokens (safe buffer)
MAX_CHARS = 1500


def split_text_at_sentences(text, max_chars):
    """Split text into chunks at sentence boundaries."""
    chunks = []
    remaining = text

    while remaining:
        if len(remaining) <= max_chars:
            chunks.append(remaining)
            break

        # Find last sentence boundary within limit
        chunk = remaining[:max_chars]
        # Look for sentence endings: . ! ? followed by space or end
        last_end = -1
        for i, char in enumerate(chunk):
            if char in '.!?' and (i + 1 >= len(chunk) or chunk[i + 1] in ' \n'):
                last_end = i + 1

        if last_end == -1:
            # No sentence boundary found, split at last space
            last_space = chunk.rfind(' ')
            if last_space > 0:
                last_end = last_space
            else:
                last_end = max_chars  # Force split

        chunks.append(remaining[:last_end].strip())
        remaining = remaining[last_end:].strip()

    return chunks


def generate_audio_chunk(client, text, model, voice, instructions, output_path):
    """Generate audio for a single chunk."""
    params = {"model": model, "voice": voice, "input": text}
    if instructions:
        params["instructions"] = instructions

    with client.audio.speech.with_streaming_response.create(**params) as response:
        response.stream_to_file(output_path)


def concatenate_audio_files(chunk_files, output_file):
    """Merge multiple MP3 files into one using ffmpeg directly."""
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        print("Error: imageio-ffmpeg package not installed. Run: pip install imageio-ffmpeg", file=sys.stderr)
        print("This is required for concatenating audio chunks.", file=sys.stderr)
        sys.exit(1)

    # Create a temporary file list for ffmpeg concat
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        list_file = f.name
        for chunk_file in chunk_files:
            # ffmpeg concat requires absolute paths with forward slashes and proper escaping
            abs_path = str(Path(chunk_file).absolute()).replace('\\', '/')
            f.write(f"file '{abs_path}'\n")

    try:
        import subprocess
        # Use ffmpeg concat demuxer to merge MP3 files
        result = subprocess.run(
            [ffmpeg_exe, '-f', 'concat', '-safe', '0', '-i', list_file, '-c', 'copy', output_file, '-y'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Error concatenating audio files: {result.stderr}", file=sys.stderr)
            sys.exit(1)
    finally:
        # Clean up the temporary file list
        Path(list_file).unlink(missing_ok=True)


def main():
    # Configure UTF-8 encoding for stdout/stderr to prevent UnicodeEncodeError on Windows
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    if len(sys.argv) < 3:
        print("Usage: python openai-tts.py <text> <output_file> [slow|normal]", file=sys.stderr)
        print("   or: python openai-tts.py --file <input_file> <output_file> [slow|normal]", file=sys.stderr)
        sys.exit(1)

    # Parse arguments - check for --file flag
    if "--file" in sys.argv:
        file_index = sys.argv.index("--file")
        input_file = sys.argv[file_index + 1]
        output_file = sys.argv[file_index + 2]
        mode = sys.argv[file_index + 3] if len(sys.argv) > file_index + 3 else None

        # Read text from file
        try:
            with open(input_file, encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: Input file not found: {input_file}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading input file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Existing behavior for backward compatibility
        text = sys.argv[1]
        output_file = sys.argv[2]
        mode = sys.argv[3] if len(sys.argv) > 3 else None

    # Find config.json relative to this script
    script_dir = Path(__file__).parent
    config_path = script_dir.parent / "references" / "config.json"

    if not config_path.exists():
        print(f"Error: Config file not found at {config_path}", file=sys.stderr)
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    tts_config = config.get("tts", {}).get("openai", {})

    # Get API key from environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set", file=sys.stderr)
        print("Set it with: export OPENAI_API_KEY='your-api-key' (Unix/macOS)", file=sys.stderr)
        print("Or: $env:OPENAI_API_KEY='your-api-key' (PowerShell)", file=sys.stderr)
        sys.exit(1)

    try:
        from openai import OpenAI
    except ImportError:
        print("Error: openai package not installed. Run: pip install openai", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(
        api_key=api_key,
        base_url=os.environ.get("OPENAI_BASE_URL", tts_config.get("api_base", "https://api.openai.com/v1"))
    )

    model = tts_config.get("model", "gpt-4o-mini-tts")
    voice = tts_config.get("voice", "coral")

    # Get instructions based on mode
    instructions = None
    if mode == "slow":
        instructions = tts_config.get("slow_instructions", "")
    elif mode == "normal":
        instructions = tts_config.get("normal_instructions", "")

    try:
        # Check if chunking needed
        if len(text) > MAX_CHARS:
            chunks = split_text_at_sentences(text, MAX_CHARS)
            print(f"Text exceeds {MAX_CHARS} chars, splitting into {len(chunks)} chunks...")

            # Generate temp files for each chunk
            temp_files = []
            output_dir = Path(output_file).parent
            for i, chunk in enumerate(chunks):
                temp_path = output_dir / f"_temp_chunk_{i}.mp3"
                generate_audio_chunk(client, chunk, model, voice, instructions, str(temp_path))
                temp_files.append(str(temp_path))
                print(f"  Generated chunk {i + 1}/{len(chunks)}")

            # Concatenate all chunks
            concatenate_audio_files(temp_files, output_file)

            # Clean up temp files
            for temp_file in temp_files:
                Path(temp_file).unlink()

            print(f"Audio saved to {output_file}")
        else:
            # Existing single-request logic
            params = {
                "model": model,
                "voice": voice,
                "input": text,
            }
            if instructions:
                params["instructions"] = instructions

            with client.audio.speech.with_streaming_response.create(**params) as response:
                response.stream_to_file(output_file)
            print(f"Audio saved to {output_file}")
    except Exception as e:
        print(f"Error generating audio: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
