from datetime import datetime

def calculate_topic_priorities(
    topics: list,
    pyq_frequencies: dict,
    weak_topics: list,
    days_until_exam: int,
    revision_history: dict = None
) -> list:
    """
    Calculates priority scores (0 to 100) for syllabus topics.
    
    Weights:
    - Weakness Score: 35%
    - PYQ Frequency Score: 30%
    - Exam Urgency Score: 20%
    - Revision Gap Score: 15%
    """
    if revision_history is None:
        revision_history = {}

    # Find maximum PYQ frequency to normalize values between 0.0 and 1.0
    max_freq = max(pyq_frequencies.values()) if pyq_frequencies and max(pyq_frequencies.values()) > 0 else 1

    # Weights configuration (Must sum to 1.0)
    W_WEAKNESS = 0.35
    W_FREQUENCY = 0.30
    W_URGENCY = 0.20
    W_REVISION = 0.15

    # Calculate Urgency Score: Fewer days remaining = Higher urgency
    # 0 to 7 days = maximum urgency (1.0), >30 days = lower urgency
    if days_until_exam <= 7:
        urgency_score = 1.0
    elif days_until_exam <= 14:
        urgency_score = 0.8
    elif days_until_exam <= 30:
        urgency_score = 0.5
    else:
        urgency_score = 0.2

    prioritized_list = []

    for topic in topics:
        # 1. Weakness Score
        is_weak = topic in weak_topics
        weakness_score = 1.0 if is_weak else 0.2

        # 2. PYQ Frequency Score (Normalized 0.0 to 1.0)
        raw_freq = pyq_frequencies.get(topic, 0)
        freq_score = raw_freq / max_freq

        # 3. Revision Gap Score
        days_since_revision = revision_history.get(topic, 999) # Default to high number if never revised
        if days_since_revision >= 14:
            revision_score = 1.0
        elif days_since_revision >= 7:
            revision_score = 0.6
        else:
            revision_score = 0.1

        # Calculate Final Priority Score (0.0 to 1.0)
        total_score = (
            (W_WEAKNESS * weakness_score) +
            (W_FREQUENCY * freq_score) +
            (W_URGENCY * urgency_score) +
            (W_REVISION * revision_score)
        )

        # Scale to 0 - 100 for readability
        final_priority = round(total_score * 100, 2)

        prioritized_list.append({
            "topic": topic,
            "priority_score": final_priority,
            "is_weak": is_weak,
            "pyq_frequency": raw_freq,
            "days_since_revision": days_since_revision,
            "explanation": f"Weakness ({weakness_score*100:.0f}%), PYQ Count ({raw_freq}), Rev Gap ({days_since_revision} days)"
        })

    # Sort topics by highest priority score first
    prioritized_list.sort(key=lambda x: x["priority_score"], reverse=True)

    return prioritized_list


# --- Testing the Priority Engine ---
if __name__ == "__main__":

    syllabus = [
        "Process Synchronization and Semaphores",
        "CPU Scheduling Algorithms",
        "Deadlock Prevention, Avoidance, and Detection",
        "Virtual Memory and Paging",
        "File System Implementation"
    ]

    # PYQ frequencies obtained from Milestone 8
    pyq_counts = {
        "Process Synchronization and Semaphores": 1,
        "CPU Scheduling Algorithms": 2,
        "Deadlock Prevention, Avoidance, and Detection": 2,
        "Virtual Memory and Paging": 1,
        "File System Implementation": 0
    }

    # Student inputs
    student_weaknesses = ["Deadlock Prevention, Avoidance, and Detection", "Virtual Memory and Paging"]
    days_to_exam = 10
    rev_gap = {
        "Process Synchronization and Semaphores": 3,   # Revised 3 days ago
        "CPU Scheduling Algorithms": 12,               # Revised 12 days ago
        "Deadlock Prevention, Avoidance, and Detection": 20, # Revised 20 days ago (Needs revision!)
        "Virtual Memory and Paging": 2,               # Revised 2 days ago
        "File System Implementation": 30               # Never revised
    }

    results = calculate_topic_priorities(
        syllabus,
        pyq_counts,
        student_weaknesses,
        days_to_exam,
        rev_gap
    )

    print("=" * 70)
    print(f"TOPIC PRIORITY RANKING (Exam in {days_to_exam} days)")
    print("=" * 70)

    for rank, item in enumerate(results, 1):
        weak_tag = "⚠️ WEAK" if item["is_weak"] else "  OK  "
        print(f"Rank {rank}: [{item['priority_score']}/100] | [{weak_tag}] | {item['topic']}")
        print(f"        Reason: {item['explanation']}\n")
        