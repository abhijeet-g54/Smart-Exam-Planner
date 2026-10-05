import pymupdf  # Modern import for PyMuPDF

def extract_text_from_pdf(pdf_path):
    print(f"Opening file: {pdf_path}")
    
    # Open the PDF file
    document = pymupdf.open(pdf_path)
    
    extracted_text = ""
    
    # Loop through every page in the PDF
    for page in document:
        text = page.get_text()
        extracted_text += text + "\n"
        
    return extracted_text

# --- Testing the function ---
if __name__ == "__main__":
    text = extract_text_from_pdf("sample.pdf")
    
    print("\n--- EXTRACTED TEXT (First 500 characters) ---\n")
    print(text[:500])