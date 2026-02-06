#!/usr/bin/env python3
"""
Edge-TTS wrapper for the Learning ESL Vocabulary skill.
Uses Python API instead of CLI to avoid command-line length limits.

Usage:
    python edge-tts-wrapper.py "text to speak" "output.mp3" [slow|normal]
    python edge-tts-wrapper.py --file "input.txt" "output.mp3" [slow|normal]

Arguments:
    text: The text to convert to speech (or --file flag for file input)
    output: Output filename (MP3)
    mode: Optional speed mode - "slow" (-10%) or "normal" (+0%)
"""

import sys
import asyncio


VOICE = "en-US-JennyNeural"
RATE_MAP = {"slow": "-10%", "normal": "+0%"}


async def generate_audio(text, output_file, rate):
    """Generate audio using edge-tts Python API."""
    try:
        import edge_tts
    except ImportError:
        print("Error: edge-tts package not installed. Run: pip install edge-tts", file=sys.stderr)
        sys.exit(1)

    communicate = edge_tts.Communicate(text, VOICE, rate=rate)
    await communicate.save(output_file)
    print(f"Audio saved to {output_file}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python edge-tts-wrapper.py <text> <output_file> [slow|normal]", file=sys.stderr)
        print("   or: python edge-tts-wrapper.py --file <input_file> <output_file> [slow|normal]", file=sys.stderr)
        sys.exit(1)

    # Parse arguments - check for --file flag
    if "--file" in sys.argv:
        file_index = sys.argv.index("--file")
        input_file = sys.argv[file_index + 1]
        output_file = sys.argv[file_index + 2]
        mode = sys.argv[file_index + 3] if len(sys.argv) > file_index + 3 else "normal"

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
        # Direct text input
        text = sys.argv[1]
        output_file = sys.argv[2]
        mode = sys.argv[3] if len(sys.argv) > 3 else "normal"

    # Get rate from mode
    rate = RATE_MAP.get(mode, "+0%")

    # Generate audio
    asyncio.run(generate_audio(text, output_file, rate))


if __name__ == "__main__":
    main()
