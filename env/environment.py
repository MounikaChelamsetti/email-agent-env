from pydantic import BaseModel
from typing import List, Optional
from .generator import generate_emails

class Observation(BaseModel):
    emails: list
    step_count: int
    history: list

class Action(BaseModel):
    action_type: str
    email_id: Optional[int] = None
    content: Optional[str] = None

class Reward(BaseModel):
    score: float
    message: str


class EmailEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.emails = generate_emails()
        self.step_count = 0
        self.history = []
        self.done = False
        return self._obs()

    def _obs(self):
        return {
            "emails": self.emails,
            "step_count": self.step_count,
            "history": self.history
        }

    def step(self, action: Action):
        self.step_count += 1
        reward = 0

        if action.action_type == "classify":
            if action.email_id == 2:
                reward += 0.5

        if action.action_type == "prioritize":
            if action.email_id in [1, 4]:
                reward += 0.5

        if action.action_type == "reply":
            reward += 0.3

        if self.step_count > 5:
            reward -= 0.2

        self.history.append(action.dict())

        if self.step_count >= 5:
            self.done = True

        return self._obs(), {"score": reward}, self.done, {}

    def state(self):
        return self._obs()
