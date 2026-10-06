from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from text_processor import clean_text

print("Loading NLP Model for Topic Mapping...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model Ready!\n")

def map_pyqs_to_topics(syllabus_topics: list, pyqs: list, threshold: float = 0.45) -> dict:
    """
    Maps Previous Year Questions (PYQs) to Syllabus Topics.
    
    Returns a dictionary with topic statistics:
    - total_questions_mapped
    - mapped_pyqs list
    - topic_frequencies (count of questions per topic)
    """
    
    # Pre-clean syllabus topics and compute their embeddings once
    cleaned_topics = [clean_text(topic) for topic in syllabus_topics]
    topic_embeddings = model.encode(cleaned_topics)
    
    # Structure to hold results
    results = {topic: [] for topic in syllabus_topics}
    
    for question in pyqs:
        cleaned_question = clean_text(question)
        question_embedding = model.encode([cleaned_question])[0]
        
        best_match_topic = None
        best_score = 0.0
        
        # Compare question against all syllabus topics
        for idx, topic in enumerate(syllabus_topics):
            score = float(cosine_similarity([question_embedding], [topic_embeddings[idx]])[0][0])
            
            if score > best_score:
                best_score = score
                best_match_topic = topic
        
        # Apply Threshold Cutoff
        if best_score >= threshold:
            results[best_match_topic].append({
                "question": question,
                "confidence_score": round(best_score, 4)
            })
            
    return results


# --- Sample Run with Realistic Operating Systems Syllabus & PYQs ---
if __name__ == "__main__":
    
    # 1. Sample Syllabus Topics for Operating Systems
    syllabus = [
        "Process Synchronization and Semaphores",
        "CPU Scheduling Algorithms",
        "Deadlock Prevention, Avoidance, and Detection",
        "Virtual Memory and Paging",
        "File System Implementation"
    ]
    
    # 2. Sample PYQs from past 3 years of exams
    past_questions = [
        "Explain Round Robin and Shortest Job First scheduling with examples.",
        "What is a Semaphore? Explain how it solves the Producer-Consumer problem.",
        "Describe Banker's Algorithm for deadlock avoidance.",
        "Differentiate between Paging and Segmentation in Virtual Memory.",
        "How to detect and recover from deadlocks in OS?",
        "Explain priority scheduling and multi-level queue scheduling.",
        "What are page faults and page replacement policies like FIFO and LRU?"
    ]
    
    print("Analyzing PYQs and mapping to Syllabus Topics...\n")
    mappings = map_pyqs_to_topics(syllabus, past_questions, threshold=0.45)
    
    # Display Results & Frequency Analysis
    print("=" * 60)
    print("PYQ TOPIC FREQUENCY ANALYSIS")
    print("=" * 60)
    
    for topic, questions in mappings.items():
        frequency = len(questions)
        print(f"\n📌 TOPIC: {topic}")
        print(f"   Frequency (Appearance Count): {frequency}")
        for item in questions:
            print(f"   - Question: \"{item['question']}\" (Confidence: {item['confidence_score']*100:.1f}%)")