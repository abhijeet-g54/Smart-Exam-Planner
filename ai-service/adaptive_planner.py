from datetime import datetime, timedelta
from priority_engine import calculate_topic_priorities
from study_plan_generator import get_sessions_needed


def rebuild_session_queue(prioritized_topics: list, completed_sessions: list) -> list:
    """
    Rebuilds the remaining study queue after removing completed sessions.

    completed_sessions example:
    [
        {"topic": "Deadlocks", "session_number": 1},
        {"topic": "Virtual Memory and Paging", "session_number": 1}
    ]
    """

    # Count how many sessions were completed for each topic
    completed_count = {}
    for item in completed_sessions:
        topic = item["topic"]
        completed_count[topic] = completed_count.get(topic, 0) + 1

    remaining_queue = []

    for item in prioritized_topics:
        topic = item["topic"]
        priority_score = item["priority_score"]
        total_needed = get_sessions_needed(priority_score)
        already_done = completed_count.get(topic, 0)

        remaining_needed = max(total_needed - already_done, 0)

        for session_number in range(already_done + 1, already_done + remaining_needed + 1):
            remaining_queue.append({
                "topic": topic,
                "priority_score": priority_score,
                "session_number": session_number,
                "total_sessions": total_needed
            })

    return remaining_queue


def adaptive_replan(
    prioritized_topics: list,
    completed_sessions: list,
    replan_start_date: str,
    exam_date: str,
    available_hours_per_day: int,
    session_duration_hours: int = 1
) -> dict:
    """
    Creates a new plan from today onward based on what is already completed.
    """

    start = datetime.strptime(replan_start_date, "%Y-%m-%d").date()
    exam = datetime.strptime(exam_date, "%Y-%m-%d").date()

    if start >= exam:
        raise ValueError("Replan start date must be before exam date.")

    sessions_per_day = available_hours_per_day // session_duration_hours
    if sessions_per_day <= 0:
        raise ValueError("Available hours per day must be at least equal to one session duration.")

    # Step 1: Build remaining queue after removing completed work
    remaining_queue = rebuild_session_queue(prioritized_topics, completed_sessions)

    # Step 2: Distribute remaining sessions across remaining days
    study_plan = []
    current_date = start
    queue_index = 0

    while current_date < exam and queue_index < len(remaining_queue):
        daily_sessions = []

        for _ in range(sessions_per_day):
            if queue_index >= len(remaining_queue):
                break

            daily_sessions.append(remaining_queue[queue_index])
            queue_index += 1

        study_plan.append({
            "date": str(current_date),
            "sessions": daily_sessions
        })

        current_date += timedelta(days=1)

    unscheduled_sessions = len(remaining_queue) - queue_index

    return {
        "replanned_schedule": study_plan,
        "remaining_sessions": len(remaining_queue),
        "unscheduled_sessions": unscheduled_sessions,
        "message": "Plan rebuilt based on completed and remaining sessions."
    }


# --- Testing Adaptive Re-planning ---
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

    # Suppose original plan started on 2026-10-07
    # Student completed only 1 Deadlock session and missed the rest of day 1
    completed_sessions = [
        {
            "topic": "Deadlock Prevention, Avoidance, and Detection",
            "session_number": 1
        }
    ]

    print("=" * 70)
    print("ADAPTIVE RE-PLANNING DEMO")
    print("=" * 70)
    print("Completed sessions:")
    for item in completed_sessions:
        print(f"  - {item['topic']} (Session {item['session_number']})")

    result = adaptive_replan(
        prioritized_topics=prioritized_topics,
        completed_sessions=completed_sessions,
        replan_start_date="2026-10-08",  # student resumes from next day
        exam_date="2026-10-17",
        available_hours_per_day=2,
        session_duration_hours=1
    )

    print("\nUpdated remaining plan:\n")
    for day in result["replanned_schedule"]:
        print(f"Date: {day['date']}")
        if not day["sessions"]:
            print("  - No sessions")
        for session in day["sessions"]:
            print(
                f"  - {session['topic']} "
                f"(Session {session['session_number']}/{session['total_sessions']}, "
                f"Priority: {session['priority_score']})"
            )
        print()

    print("=" * 70)
    print(f"Remaining sessions: {result['remaining_sessions']}")
    print(f"Unscheduled sessions: {result['unscheduled_sessions']}")
    print(f"Message: {result['message']}")
    print("=" * 70)