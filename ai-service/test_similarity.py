from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading AI Embedding Model... (This takes a few seconds on first run)")
# Load lightweight open-source model from HuggingFace
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded successfully!\n")

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Computes semantic similarity score (0.0 to 1.0) between two text strings.
    """
    # Convert texts into 384-dimensional numerical vectors (embeddings)
    embeddings = model.encode([text1, text2])
    
    # Calculate Cosine Similarity between the two vectors
    similarity_score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    
    return float(similarity_score)


# --- Testing Semantic Similarity ---
if __name__ == "__main__":
    syllabus_topic = "Deadlock Prevention and Avoidance"
    
    pyq_questions = [
        "Explain techniques used to prevent deadlocks in operating systems.", # High match expected
        "What is Bankers Algorithm for avoiding deadlocks?",                   # High match expected
        "How does virtual memory paging work?",                                # Low match expected
        "What is SQL JOIN operation?"                                         # Zero match expected
    ]
    
    print(f"--- SYLLABUS TOPIC: '{syllabus_topic}' ---\n")
    
    for q in pyq_questions:
        score = calculate_similarity(syllabus_topic, q)
        percentage = round(score * 100, 2)
        print(f"PYQ: \"{q}\"")
        print(f"--> Similarity Score: {score:.4f} ({percentage}% match)\n") 