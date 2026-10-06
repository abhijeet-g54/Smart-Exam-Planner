from datetime import datetime, timedelta
from priority_engine import calculate_topic_priorities


def get_sessions_needed(priority_score: float) -> int:
    """
    Decides how many study sessions a topic needs based on its priority score.
    """
    if priority_score >= 80:
        return 3
    elif priority_score >= 60:
        return 2
    else:
        return 1


def generate_study_plan(
    prioritized_topics: list,
    start_date: str,
    exam_date: str,
    available_hours_per_day: int,
    session_duration_hours: int = 1
) -> list:
    """
    Generates a simple day-wise study plan.

    Inputs:
    - prioritized_topics: list returned by priority_engine
    - start_date: planning start date in YYYY-MM-DD format
    - exam_date: exam date in YYYY-MM-DD format
    - available_hours_per_day: how many hours student can study daily
    - session_duration_hours: duration of one study session

    Output:
    - list of daily schedules
    """

    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    exam = datetime.strptime(exam_date, "%Y-%m-%d").date()

    if start >= exam:
        raise ValueError("Start date must be before exam date.")

    sessions_per_day = available_hours_per_day // session_duration_hours

    if sessions_per_day <= 0:
        raise ValueError("Available hours per day must be at least equal to session duration.")

    # Step 1: Create a queue of study sessions based on topic priority
    study_queue = []

    for item in prioritized_topics:
        topic = item["topic"]
        priority_score = item["priority_score"]
        sessions_needed = get_sessions_needed(priority_score)

        for session_number in range(1, sessions_needed + 1):
            study_queue.append({
                "topic": topic,
                "priority_score": priority_score,
                "session_number": session_number,
                "total_sessions": sessions_needed
            })

    # Step 2: Distribute sessions across days
    study_plan = []
    current_date = start
    queue_index = 0

    while current_date < exam and queue_index < len(study_queue):
        daily_sessions = []

        for _ in range(sessions_per_day):
            if queue_index >= len(study_queue):
                break

            daily_sessions.append(study_queue[queue_index])
            queue_index += 1

        study_plan.append({
            "date": str(current_date),
            "sessions": daily_sessions
        })

        current_date += timedelta(days=1)

    # Step 3: Check if all sessions were scheduled
    unscheduled_sessions = len(study_queue) - queue_index

    return {
        "study_plan": study_plan,
        "total_sessions_required": len(study_queue),
        "unscheduled_sessions": unscheduled_sessions
    }


# --- Testing Study Plan Generation ---
if __name__ == "__main__":

    syllabus = [
        "Process Synchronization and Semaphores",
        "CPU Scheduling Algorithms",
        "Deadlock Prevention, Avoidance, and Detection",
        "Virtual Memory and Paging",
        "File System Implementation"
    ]

    pyq_counts = {
        "Process Synchronization and Semaphores": 1,
        "CPU Scheduling Algorithms": 2,
        "Deadlock Prevention, Avoidance, and Detection": 2,
        "Virtual Memory and Paging": 1,
        "File System Implementation": 0
    }

    student_weaknesses = [
        "Deadlock Prevention, Avoidance, and Detection",
        "Virtual Memory and Paging"
    ]

    days_to_exam = 10

    revision_gap = {
        "Process Synchronization and Semaphores": 3,
        "CPU Scheduling Algorithms": 12,
        "Deadlock Prevention, Avoidance, and Detection": 20,
        "Virtual Memory and Paging": 2,
        "File System Implementation": 30
    }

    prioritized_topics = calculate_topic_priorities(
        syllabus,
        pyq_counts,
        student_weaknesses,
        days_to_exam,
        revision_gap
    )

    result = generate_study_plan(
        prioritized_topics=prioritized_topics,
        start_date="2026-10-07",
        exam_date="2026-10-17",
        available_hours_per_day=2,
        session_duration_hours=1
    )

    print("=" * 70)
    print("GENERATED STUDY PLAN")
    print("=" * 70)

    for day in result["study_plan"]:
        print(f"\nDate: {day['date']}")
        for session in day["sessions"]:
            print(
                f"  - {session['topic']} "
                f"(Session {session['session_number']}/{session['total_sessions']}, "
                f"Priority: {session['priority_score']})"
            )

    print("\n" + "=" * 70)
    print(f"Total sessions required: {result['total_sessions_required']}")
    print(f"Unscheduled sessions: {result['unscheduled_sessions']}")
    print("=" * 70)