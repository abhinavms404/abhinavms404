#!/usr/bin/env python3
"""
SVG Banner Builder for GitHub Profile

Reads ASCII art from a text file, injects it into SVG templates,
and produces the final dark and light themed banners.

Usage:
    python scripts/build_svg.py [--art assets/avatar.txt]

Produces:
    assets/dark.svg
    assets/light.svg
"""

import sys
import os
import argparse

# SVG rendering constants
FONT_SIZE = 6.5
X_OFFSET = 70
Y_START = 5
Y_INCREMENT = 8
GLITCH_LINE = 4  # 0-indexed line used in the glitch overlay (line 5 of art)


def read_ascii(path):
    """Read ASCII art from file, preserving empty lines."""
    if not os.path.exists(path):
        print(f"Error: ASCII art file not found: {path}")
        sys.exit(1)

    with open(path) as f:
        lines = [line.rstrip("\n") for line in f.readlines()]

    return lines


def make_tspan(line, line_num):
    """Generate a single SVG tspan element for one line of ASCII art."""
    y = Y_START + line_num * Y_INCREMENT
    # Escape XML special chars
    escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")
    return f'        <tspan x="{X_OFFSET}" y="{y}">{escaped}</tspan>'


def build_svg(template_path, art_lines, output_path, glitch_line_idx=4):
    """
    Read the SVG template, replace {{ASCII_ART}} with generated tspans,
    and write the final SVG.

    The template must contain exactly one {{ASCII_ART}} placeholder.
    """
    if not os.path.exists(template_path):
        print(f"Error: Template not found: {template_path}")
        sys.exit(1)

    with open(template_path) as f:
        template = f.read()

    if "{{ASCII_ART}}" not in template:
        print(f"Error: Template missing {{ASCII_ART}} placeholder: {template_path}")
        sys.exit(1)

    # Build the tspan block
    tspan_lines = []
    for i, line in enumerate(art_lines):
        tspan_lines.append(make_tspan(line, i))

    art_block = "\n".join(tspan_lines)

    result = template.replace("{{ASCII_ART}}", art_block)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w") as f:
        f.write(result)

    print(f"Built: {output_path} ({len(art_lines)} art lines)")


def main():
    parser = argparse.ArgumentParser(description="Build SVG banners from ASCII art")
    parser.add_argument(
        "--art",
        default="assets/avatar.txt",
        help="Path to ASCII art file (default: assets/avatar.txt)",
    )
    args = parser.parse_args()

    art_lines = read_ascii(args.art)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(base_dir, "assets")

    # Build dark and light SVGs
    build_svg(
        os.path.join(assets_dir, "dark.template.svg"),
        art_lines,
        os.path.join(assets_dir, "dark.svg"),
    )
    build_svg(
        os.path.join(assets_dir, "light.template.svg"),
        art_lines,
        os.path.join(assets_dir, "light.svg"),
    )

    print("Done. Both SVGs updated.")


if __name__ == "__main__":
    main()
