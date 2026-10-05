import re

def clean_text(raw_text: str) -> str:
    """
    Cleans raw text extracted from PDFs or OCR images.
    
    Steps:
    1. Removes unwanted special symbols (keeps standard text, numbers, punctuation).
    2. Replaces multiple line breaks and tab characters with a single space.
    3. Replaces multiple spaces with a single space.
    4. Converts to lowercase.
    """
    if not raw_text:
        return ""
    
    # 1. Remove non-ASCII/garbage characters often produced by OCR
    cleaned = raw_text.encode("ascii", errors="ignore").decode("utf-8")
    
    # 2. Replace line breaks, carriage returns, tabs with spaces
    cleaned = re.sub(r'[\r\n\t]+', ' ', cleaned)
    
    # 3. Remove standalone page indicators like "Page 1", "- 12 -", etc.
    cleaned = re.sub(r'(?i)\bpage\s+\d+\b', '', cleaned)
    
    # 4. Replace multiple spaces with a single space
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # 5. Convert to lowercase and strip outer whitespace
    cleaned = cleaned.lower().strip()
    
    return cleaned


# --- Testing the cleaning module ---
if __name__ == "__main__":
    sample_messy_text = """
    MODULE 2:   Operating Systems   --- Page 12 ---
    
    What is a DEADLOCK?
    A deadlock is a situation where a set of processes are blocked...
    
    Key conditions:
    \t1. Mutual Exclusion
    \t2. Hold and Wait
    \t3. No Preemption
    \t4. Circular Wait
    
    @#$ Garbage OCR Noise %^*&
    """
    
    print("--- ORIGINAL MESSY TEXT ---")
    print(sample_messy_text)
    
    cleaned_result = clean_text(sample_messy_text)
    
    print("\n--- CLEANED TEXT ---")
    print(cleaned_result)
    