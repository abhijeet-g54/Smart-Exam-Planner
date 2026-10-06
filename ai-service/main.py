from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

# Import our custom modular components
from text_processor import clean_text
from topic_mapper import map_pyqs_to_topics
from priority_engine import calculate_topic_priorities
from study_plan_generator import generate_study_plan
from adaptive_planner import adaptive_replan

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered Adaptive Exam Planner Service",
    description="Python microservice providing NLP topic mapping, priority calculation, and adaptive study scheduling.",
    version="1.0.0"
)

# --- REQUEST & RESPONSE SCHEMAS (Pydantic Models) ---

class TopicMappingRequest(BaseModel):
    syllabus_topics: List[str]
    pyqs: List[str]
    threshold: Optional[float] = 0.45

class PriorityRequest(BaseModel):
    topics: List[str]
    pyq_frequencies: Dict[str, int]
    weak_topics: List[str]
    days_until_exam: int
    revision_history: Optional[Dict[str, int]] = {}

class StudyPlanRequest(BaseModel):
    prioritized_topics: List[Dict]
    start_date: str
    exam_date: str
    available_hours_per_day: int
    session_duration_hours: Optional[int] = 1

class AdaptiveReplanRequest(BaseModel):
    prioritized_topics: List[Dict]
    completed_sessions: List[Dict]
    replan_start_date: str
    exam_date: str
    available_hours_per_day: int
    session_duration_hours: Optional[int] = 1


# --- REST API ENDPOINTS ---

@app.get("/health")
def health_check():
    """Simple endpoint to verify that the FastAPI service is running."""
    return {"status": "UP", "service": "AI/ML FastAPI Engine"}


@app.post("/api/ai/clean-text")
def api_clean_text(payload: Dict[str, str]):
    """Cleans raw text extracted from documents/OCR."""
    raw_text = payload.get("text", "")
    return {"cleaned_text": clean_text(raw_text)}


@app.post("/api/ai/map-pyqs")
def api_map_pyqs(request: TopicMappingRequest):
    """Maps Previous Year Questions (PYQs) to Syllabus Topics using Sentence Transformers."""
    try:
        mapping_result = map_pyqs_to_topics(
            request.syllabus_topics,
            request.pyqs,
            request.threshold
        )
        return {"status": "success", "mapping": mapping_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ai/calculate-priority")
def api_calculate_priority(request: PriorityRequest):
    """Calculates explainable priority scores for all syllabus topics."""
    try:
        priorities = calculate_topic_priorities(
            topics=request.topics,
            pyq_frequencies=request.pyq_frequencies,
            weak_topics=request.weak_topics,
            days_until_exam=request.days_until_exam,
            revision_history=request.revision_history
        )
        return {"status": "success", "prioritized_topics": priorities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ai/generate-plan")
def api_generate_plan(request: StudyPlanRequest):
    """Generates an initial day-wise study schedule."""
    try:
        plan = generate_study_plan(
            prioritized_topics=request.prioritized_topics,
            start_date=request.start_date,
            exam_date=request.exam_date,
            available_hours_per_day=request.available_hours_per_day,
            session_duration_hours=request.session_duration_hours
        )
        return {"status": "success", "data": plan}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/ai/replan")
def api_replan(request: AdaptiveReplanRequest):
    """Re-plans remaining study sessions based on student progress and missed days."""
    try:
        replanned_result = adaptive_replan(
            prioritized_topics=request.prioritized_topics,
            completed_sessions=request.completed_sessions,
            replan_start_date=request.replan_start_date,
            exam_date=request.exam_date,
            available_hours_per_day=request.available_hours_per_day,
            session_duration_hours=request.session_duration_hours
        )
        return {"status": "success", "data": replanned_result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    