# AI Microservice API Specifications

**Base URL:** `http://localhost:8000`  
**Content-Type:** `application/json`

---

## 1. Health Check
- **Method:** `GET`
- **Endpoint:** `/health`
- **Purpose:** Verifies whether the Python AI service is running.
- **Response:**
```json
{
  "status": "UP",
  "service": "AI/ML FastAPI Engine"
}