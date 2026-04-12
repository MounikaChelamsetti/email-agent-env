from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict, Optional

from env.environment import EmailEnv, Action
from env.grader import grade_easy, grade_medium, grade_hard
from env.generator import generate_emails

app = FastAPI()
env = EmailEnv()

@app.get("/")
def home():
    return {"message": "Running"}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "email-agent-env"}

@app.post("/reset")
def reset():
    return env.reset()

@app.get("/reset")
def reset_get():
    return env.reset()

@app.post("/step")
def step(action: Action):
    state, reward, done, info = env.step(action)
    return {"state": state, "reward": reward, "done": done, "info": info}

@app.get("/state")
def get_state():
    return env.state()

@app.get("/tasks")
def list_tasks():
    return {"tasks": [
        {
            "id": "easy",
            "name": "Urgent Email Prioritization",
            "description": "Identify and prioritize the urgent email.",
            "grader_fn": "grade_easy"
        },
        {
            "id": "medium",
            "name": "Spam Detection",
            "description": "Classify spam correctly without false positives.",
            "grader_fn": "grade_medium"
        },
        {
            "id": "hard",
            "name": "Mixed Inbox Management",
            "description": "Prioritize urgent, classify spam, reply to normal.",
            "grader_fn": "grade_hard"
        },
    ]}

GRADERS = {"easy": grade_easy, "medium": grade_medium, "hard": grade_hard}

class GraderRequest(BaseModel):
    task_id: str
    state: Optional[Dict[str, Any]] = None
    episode_id: Optional[str] = None

@app.post("/grader")
def grader(req: GraderRequest):
    fn = GRADERS.get(req.task_id)
    if fn is None:
        return {"error": f"Unknown task_id: {req.task_id}", "score": 0.001}

    # Always build a state with real emails so score is never edge-case
    raw = req.state or {}
    if not raw or not raw.get("emails"):
        raw = {
            "emails": generate_emails(),
            "actions": [],
            "history": []
        }
    # normalize history -> actions
    if "history" in raw and "actions" not in raw:
        raw["actions"] = raw["history"]
    elif "history" in raw:
        raw["actions"] = raw["actions"] or raw["history"]

    score = fn(raw)
    # Hard guarantee: never 0.0 or 1.0
    score = max(0.001, min(0.999, float(score)))
    return {"task_id": req.task_id, "score": score}