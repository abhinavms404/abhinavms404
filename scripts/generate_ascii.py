#!/usr/bin/env python3
"""
ASCII Art Generator for GitHub Profile

Reads a profile image, converts to grayscale, maps brightness to ASCII
characters, and saves the result as a text file.

Usage:
    python scripts/generate_ascii.py <input_image> [output_file]

Defaults:
    input_image: assets/profile.jpg
    output_file: assets/avatar.txt
"""

import sys
import os

try:
    from PIL import Image
except ImportError:
    print("Error: PIL (Pillow) is required. Install with: pip install Pillow")
    sys.exit(1)

# ASCII ramp from darkest to lightest
ASCII_CHARS = "@%#*+=-:. "


def image_to_ascii(image_path, output_width=100):
    """
    Convert an image to ASCII art.

    Args:
        image_path: Path to the input image
        output_width: Width in characters of the output ASCII art

    Returns:
        List of strings, each string is a row of ASCII characters
    """
    if not os.path.exists(image_path):
        print(f"Error: Image not found: {image_path}")
        sys.exit(1)

    img = Image.open(image_path)

    # Convert to grayscale
    img = img.convert("L")

    # Calculate height preserving aspect ratio
    aspect = img.height / img.width
    output_height = int(output_width * aspect * 0.5)

    # Resize
    img = img.resize((output_width, output_height))

    pixels = list(img.getdata())

    rows = []
    for i in range(0, len(pixels), output_width):
        row_pixels = pixels[i : i + output_width]
        row = "".join(
            ASCII_CHARS[min(pixel * len(ASCII_CHARS) // 256, len(ASCII_CHARS) - 1)]
            for pixel in row_pixels
        )
        rows.append(row)

    return rows


def save_ascii(rows, output_path="assets/avatar.txt"):
    """Save ASCII art rows to a text file."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w") as f:
        for row in rows:
            f.write(row + "\n")
    print(f"ASCII art saved to {output_path} ({len(rows)} rows x {len(rows[0])} cols)")


if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "assets/profile.jpg"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "assets/avatar.txt"
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 100

    rows = image_to_ascii(input_path, output_width=width)
    save_ascii(rows, output_path)
