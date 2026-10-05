import pytesseract
from PIL import Image
import os

# --- IMPORTANT FOR WINDOWS USERS ---
# We point pytesseract directly to where Tesseract is installed.
# This avoids "TesseractNotFoundError" on Windows computers.
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

def extract_text_from_image(image_path):
    print(f"Opening image: {image_path}")
    
    # Open image using Pillow library
    img = Image.open(image_path)
    
    # Run Tesseract OCR on the image
    extracted_text = pytesseract.image_to_string(img)
    
    return extracted_text

# --- Testing the function ---
if __name__ == "__main__":
    image_filename = "sample_ocr.png" # Change to sample_ocr.jpg if you used a JPG
    
    if not os.path.exists(image_filename):
        print(f"Error: File '{image_filename}' not found in ai-service folder!")
    else:
        text = extract_text_from_image(image_filename)
        
        print("\n--- EXTRACTED TEXT FROM OCR ---\n")
        print(text)