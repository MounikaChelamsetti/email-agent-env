# In your server/app.py (add these if missing)
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# Make sure these routes exist:

@app.get("/tasks")
def get_tasks():
    return {
        "tasks": [
            {
                "id": "easy",
                "description": "Handle a simple normal email",
                "grader_fn": "grade_easy"
            },
            {
                "id": "medium", 
                "description": "Handle an urgent email correctly",
                "grader_fn": "grade_medium"
            },
            {
                "id": "hard",
                "description": "Handle spam detection and classification",
                "grader_fn": "grade_hard"
            }
        ]
    }


class GraderRequest(BaseModel):
    task_id: str
    episode_id: Optional[str] = None


@app.post("/grader")
def run_grader(request: GraderRequest):
    from env.grader import grade_easy, grade_medium, grade_hard
    
    # Get current state from your environment
    state = your_env_instance.get_state()  # replace with your actual state getter
    trajectory = []  # pass trajectory if you track it

    graders = {
        "easy": grade_easy,
        "medium": grade_medium,
        "hard": grade_hard,
    }

    fn = graders.get(request.task_id)
    if fn is None:
        return {"error": f"Unknown task_id: {request.task_id}"}, 400

    score = fn(state, trajectory)
    return {"score": score, "task_id": request.task_id}
