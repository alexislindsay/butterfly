#!/usr/bin/env python3
import sys
import os
from PyPDF2 import PdfReader

def pdf_to_txt(pdf_path, output_txt):
    reader = PdfReader(pdf_path)
    all_text = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            all_text.append(text.strip())
        else:
            print(f"Warning: Page {i + 1} is empty or unreadable.")

    full_text = '\n\n'.join(all_text)

    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(full_text)

    print(f"✔ Converted '{pdf_path}' → '{output_txt}' ({len(reader.pages)} pages)")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pdftotxt.py /path/to/source.pdf /path/to/output.txt")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_txt = sys.argv[2]

    if not os.path.isfile(pdf_path):
        print(f"Error: '{pdf_path}' does not exist.")
        sys.exit(1)

    pdf_to_txt(pdf_path, output_txt)
