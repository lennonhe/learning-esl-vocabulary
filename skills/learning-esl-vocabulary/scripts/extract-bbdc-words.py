"""
Extract vocabulary words from BBDC PDF exports.
Usage: python extract_bbdc_words.py <pdf_path_or_url>

This script handles:
- Chinese text filtering (headers/footers)
- Two-column layout parsing with position-based word assignment
- Multi-line phrase joining using y-position proximity with threshold
- Number and header filtering
- URL download support (http:// or https://)
"""
import os
import re
import sys
import urllib.request
import urllib.parse
from datetime import datetime

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber is required. Install with: pip install pdfplumber", file=sys.stderr)
    sys.exit(1)


def is_url(path):
    """Check if path is a URL."""
    return path.startswith(('http://', 'https://'))


def extract_filename_from_url(url):
    """Extract and decode filename from URL."""
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    filename = urllib.parse.unquote(path.split('/')[-1])

    if not filename.lower().endswith('.pdf'):
        filename += '.pdf'

    # Sanitize invalid characters for Windows/Unix filenames
    for char in '<>:"/\\|?*':
        filename = filename.replace(char, '_')

    return filename if filename else 'downloaded.pdf'


def download_pdf(url, download_dir):
    """Download PDF from URL to local directory."""
    os.makedirs(download_dir, exist_ok=True)

    filename = extract_filename_from_url(url)
    local_path = os.path.join(download_dir, filename)

    # Create request with user agent header
    request = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (ESL Vocabulary Tool)'}
    )

    # Download the file
    with urllib.request.urlopen(request, timeout=30) as response:
        with open(local_path, 'wb') as f:
            f.write(response.read())

    # Validate it's a PDF
    with open(local_path, 'rb') as f:
        if f.read(5) != b'%PDF-':
            os.remove(local_path)
            raise ValueError("Downloaded file is not a valid PDF")

    return local_path, filename


def extract_words_with_positions(pdf_path):
    """Extract words with their x and y positions from PDF."""
    all_items = []  # List of (y_pos, items) where items is list of {text, x0, x1}
    PAGE_HEIGHT = 1000  # Approximate page height for offset calculation

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            words = page.extract_words() or []
            # Group words by their top position (same line)
            lines = {}
            for w in words:
                # Add page offset to make y-positions unique across pages
                top = round(w['top'], 1) + page_num * PAGE_HEIGHT
                if top not in lines:
                    lines[top] = []
                lines[top].append({
                    'text': w['text'],
                    'x0': w['x0'],
                    'x1': w['x1']
                })

            # Sort lines by top position, then words by x position
            for top in sorted(lines.keys()):
                line_words = sorted(lines[top], key=lambda w: w['x0'])
                all_items.append((top, line_words))

    return all_items


def is_chinese(text):
    """Check if text contains Chinese characters."""
    return bool(re.search(r'[\u4e00-\u9fff\u2f00-\u2fff]', text))


def is_entry_number(text, max_num=10000):
    """Check if text is a valid entry number."""
    return text.isdigit() and 1 <= int(text) <= max_num


def parse_vocabulary_with_positions(all_items):
    """Parse vocabulary using word positions to determine column assignment."""
    entries = {}
    Y_THRESHOLD = 25  # Maximum y-distance for word-number association

    # First pass: find the typical x-position boundary between columns
    x_boundaries = []
    for y_pos, line_words in all_items:
        numbers = [(i, w) for i, w in enumerate(line_words) if is_entry_number(w['text'])]
        if len(numbers) == 2:
            x_boundaries.append((numbers[0][1]['x1'] + numbers[1][1]['x0']) / 2)

    col_boundary = sorted(x_boundaries)[len(x_boundaries) // 2] if x_boundaries else 200

    # Second pass: find all entry numbers and their y-positions
    left_numbers = {}  # num -> y_pos
    right_numbers = {}
    for y_pos, line_words in all_items:
        if any(is_chinese(w['text']) for w in line_words):
            continue
        left_words = [w for w in line_words if w['x0'] < col_boundary]
        right_words = [w for w in line_words if w['x0'] >= col_boundary]
        for w in left_words:
            if is_entry_number(w['text']):
                left_numbers[int(w['text'])] = y_pos
        for w in right_words:
            if is_entry_number(w['text']):
                right_numbers[int(w['text'])] = y_pos

    # Third pass: assign words to entries based on proximity with threshold
    for y_pos, line_words in all_items:
        if any(is_chinese(w['text']) for w in line_words):
            continue
        line_text = ' '.join(w['text'] for w in line_words)
        if 'Word' in line_text and 'Meaning' in line_text:
            continue

        left_words = [w for w in line_words if w['x0'] < col_boundary]
        right_words = [w for w in line_words if w['x0'] >= col_boundary]

        # Process left column
        left_texts = [w['text'] for w in left_words if not is_entry_number(w['text'])]
        if left_texts:
            # Find the closest entry number within threshold
            closest_num = None
            min_dist = float('inf')
            for num, num_y in left_numbers.items():
                dist = abs(y_pos - num_y)
                if dist < min_dist and dist <= Y_THRESHOLD:
                    min_dist = dist
                    closest_num = num
            if closest_num is not None:
                word = ' '.join(left_texts)
                if closest_num in entries:
                    # Check if this word should be prepended or appended
                    if y_pos < left_numbers[closest_num]:
                        entries[closest_num] = word + ' ' + entries[closest_num]
                    else:
                        entries[closest_num] = entries[closest_num] + ' ' + word
                else:
                    entries[closest_num] = word

        # Process right column
        right_texts = [w['text'] for w in right_words if not is_entry_number(w['text'])]
        if right_texts:
            closest_num = None
            min_dist = float('inf')
            for num, num_y in right_numbers.items():
                dist = abs(y_pos - num_y)
                if dist < min_dist and dist <= Y_THRESHOLD:
                    min_dist = dist
                    closest_num = num
            if closest_num is not None:
                word = ' '.join(right_texts)
                if closest_num in entries:
                    if y_pos < right_numbers[closest_num]:
                        entries[closest_num] = word + ' ' + entries[closest_num]
                    else:
                        entries[closest_num] = entries[closest_num] + ' ' + word
                else:
                    entries[closest_num] = word

    # Sort by entry number and return as list
    sorted_entries = sorted(entries.items(), key=lambda x: x[0])
    return [word for num, word in sorted_entries]


def extract_words(pdf_path):
    """Extract vocabulary words from BBDC PDF export."""
    all_items = extract_words_with_positions(pdf_path)
    return parse_vocabulary_with_positions(all_items)


if __name__ == '__main__':
    # Configure UTF-8 encoding for stdout/stderr to prevent UnicodeEncodeError on Windows
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    if len(sys.argv) != 2:
        print("Usage: python extract_bbdc_words.py <pdf_path_or_url>", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    local_path = input_path
    original_filename = None

    # Handle URL download
    if is_url(input_path):
        today = datetime.now().strftime('%Y-%m-%d')
        download_dir = os.path.join('bbdc-review', 'downloads', today)

        print(f"Downloading PDF from URL...")
        try:
            local_path, original_filename = download_pdf(input_path, download_dir)
            print(f"Downloaded to: {local_path}")
        except Exception as e:
            print(f"Error downloading PDF: {e}", file=sys.stderr)
            sys.exit(1)

    # Extract words from the PDF
    words = extract_words(local_path)

    print(f"Extracted {len(words)} words:")
    for i, word in enumerate(words, 1):
        print(f"{i}. {word}")

    # Output metadata for SKILL.md to use when processing URLs
    if original_filename:
        print(f"\n[SOURCE_FILE]: {local_path}")
        print(f"[PDF_BASENAME]: {original_filename.rsplit('.', 1)[0]}")
