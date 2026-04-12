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
            "grader": "grade_easy",
            "grader_fn": "grade_easy"
        },
        {
            "id": "medium",
            "name": "Spam Detection",
            "description": "Classify spam correctly without false positives.",
            "grader": "grade_medium",
            "grader_fn": "grade_medium"
        },
        {
            "id": "hard",
            "name": "Mixed Inbox Management",
            "description": "Prioritize urgent, classify spam, reply to normal.",
            "grader": "grade_hard",
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
    """Legacy grader endpoint for backward compatibility."""
    fn = GRADERS.get(req.task_id)
    if fn is None:
        return {"error": f"Unknown task_id: {req.task_id}", "score": 0.001}

    raw = req.state or {}
    if not raw or not raw.get("emails"):
        raw = {
            "emails": generate_emails(),
            "actions": [],
            "history": []
        }

    if isinstance(raw, dict) and "history" in raw and "actions" not in raw:
        raw["actions"] = raw["history"]
    elif isinstance(raw, dict) and "history" in raw:
        raw["actions"] = raw.get("actions") or raw["history"]

    score = fn(raw if isinstance(raw, dict) else {})
    score = max(0.001, min(0.999, float(score)))

    return {"task_id": req.task_id, "score": float(score)}


@app.post("/grade")
def grade_task(task_id: str, state: Dict[str, Any]):
    """Grade a task based on its id and the final state."""
    grader_fn = GRADERS.get(task_id)
    
    if grader_fn is None:
        return {"error": f"Unknown task: {task_id}", "score": 0.001}
    
    # Convert history to actions if needed
    if isinstance(state, dict) and "history" in state and "actions" not in state:
        state["actions"] = state["history"]
    
    score = grader_fn(state if isinstance(state, dict) else {})
    
    # Validate score is strictly between 0 and 1
    if not (0 < score < 1):
        score = max(0.001, min(0.999, float(score)))
    
    return {"task_id": task_id, "score": float(score)}


@app.get("/validate")
def validate_submission():
    """Validate that the submission meets HuggingFace Space requirements."""
    
    validation_results = {
        "has_3_tasks": False,
        "all_graders_valid": False,
        "all_scores_in_range": True,
        "errors": [],
        "warnings": [],
        "tasks": []
    }
    
    # Test state
    test_state = {"actions": [], "emails": [
        {"id": 1, "is_urgent": True, "is_spam": False},
        {"id": 2, "is_urgent": False, "is_spam": True},
        {"id": 3, "is_urgent": False, "is_spam": False},
        {"id": 4, "is_urgent": True, "is_spam": False}
    ]}
    
    tasks_to_test = ["easy", "medium", "hard"]
    
    # Check 1: At least 3 tasks
    if len(tasks_to_test) >= 3:
        validation_results["has_3_tasks"] = True
    else:
        validation_results["errors"].append(f"Expected at least 3 tasks, found {len(tasks_to_test)}")
    
    # Check 2: Test each grader
    for task_id in tasks_to_test:
        try:
            grader_fn = GRADERS.get(task_id)
            if grader_fn is None:
                validation_results["errors"].append(f"Grader not found for task '{task_id}'")
                continue
            
            score = grader_fn(test_state)
            
            task_info = {
                "id": task_id,
                "score": float(score),
                "valid": False
            }
            
            if isinstance(score, (int, float)):
                if 0 < score < 1:
                    task_info["valid"] = True
                else:
                    validation_results["errors"].append(
                        f"Task '{task_id}' returned score {score} which is not strictly between 0 and 1"
                    )
                    validation_results["all_scores_in_range"] = False
            else:
                validation_results["errors"].append(f"Task '{task_id}' returned non-numeric score: {type(score)}")
            
            validation_results["tasks"].append(task_info)
            
        except Exception as e:
            validation_results["errors"].append(f"Task '{task_id}' grader failed: {str(e)}")
    
    # Final validation
    validation_results["all_graders_valid"] = (
        validation_results["has_3_tasks"] and 
        validation_results["all_scores_in_range"] and 
        len(validation_results["errors"]) == 0
    )
    
    return validation_results
