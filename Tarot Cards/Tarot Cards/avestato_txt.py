import pdfplumber

pdf_path = r"C:\Users\alexi\Downloads\Tarot Cards\Avesta, The Sacred Books of The Parsis (Karl Friedrich Geldner) (Z-Library).pdf"
output_path = r"C:\Users\alexi\moon-ui\src\data\avesta.txt"

with pdfplumber.open(pdf_path) as pdf:
    full_text = ''
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            full_text += text + '\n\n'

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(full_text)

print(f"✅ Avesta extracted to: {output_path}")
