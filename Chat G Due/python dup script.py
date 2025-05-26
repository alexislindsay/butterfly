from PyPDF2 import PdfReader, PdfWriter

# Paths to the input and output PDF files
input_pdf_path = r"C:\Users\alexi\Downloads\journal stub.pdf"  # Your original file path
output_pdf_path = r"C:\Users\alexi\Downloads\Expanded_Journal_730_Pages.pdf"  # Desired output file path

# Load the original PDF
reader = PdfReader(input_pdf_path)
writer = PdfWriter()

# Define the target number of pages
target_page_count = 730
original_pages = reader.pages

# Duplicate pages to reach the target page count
while len(writer.pages) < target_page_count:
    for page in original_pages:
        writer.add_page(page)
        if len(writer.pages) >= target_page_count:
            break

# Save the duplicated PDF
with open(output_pdf_path, "wb") as output_pdf:
    writer.write(output_pdf)

print("PDF expanded to 730 pages and saved as:", output_pdf_path)
