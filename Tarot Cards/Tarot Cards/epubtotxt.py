#!/usr/bin/env python3
import sys
import os
from ebooklib import epub, ITEM_DOCUMENT   # ← import ITEM_DOCUMENT here
from bs4 import BeautifulSoup

def epub_to_txt(epub_path, output_txt):
    book = epub.read_epub(epub_path)
    all_text = []

    for item in book.get_items():  
        # use the standalone ITEM_DOCUMENT constant
        if item.get_type() == ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            chapter_text = soup.get_text(separator='\n')
            all_text.append(chapter_text.strip())

    full_text = '\n\n'.join(all_text)
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(full_text)

    print(f"Converted '{epub_path}' → '{output_txt}' ({len(all_text)} sections)")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python epubtotxt.py /path/to/source.epub /path/to/output.txt")
        sys.exit(1)

    epub_path = sys.argv[1]
    output_txt = sys.argv[2]

    if not os.path.isfile(epub_path):
        print(f"Error: '{epub_path}' does not exist.")
        sys.exit(1)

    epub_to_txt(epub_path, output_txt)
