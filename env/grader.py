from typing import Any, Dict, List


def _clamp(score: float) -> float:
    # ensures strictly between (0,1)
    return max(0.05, min(0.95, float(score)))


# 🟢 EASY TASK
def grade_easy(state: Dict[str, Any], trajectory: List[Dict[str, Any]]) -> float:
    try:
        actions = trajectory or state.get("history", [])
        if not actions:
            return 0.2

        score = 0.3

        if any(a.get("action_type") == "prioritize" for a in actions):
            score += 0.4

        return _clamp(score)

    except Exception:
        return 0.2


# 🟡 MEDIUM TASK
def grade_medium(state: Dict[str, Any], trajectory: List[Dict[str, Any]]) -> float:
    try:
        actions = trajectory or state.get("history", [])
        if not actions:
            return 0.3

        score = 0.3

        if any(a.get("action_type") == "classify" for a in actions):
            score += 0.4

        return _clamp(score)

    except Exception:
        return 0.3


# 🔴 HARD TASK
def grade_hard(state: Dict[str, Any], trajectory: List[Dict[str, Any]]) -> float:
    try:
        actions = trajectory or state.get("history", [])
        if not actions:
            return 0.4

        score = 0.3

        action_types = {a.get("action_type") for a in actions}

        if "prioritize" in action_types:
            score += 0.2
        if "classify" in action_types:
            score += 0.2
        if "reply" in action_types:
            score += 0.2

        return _clamp(score)

    except Exception:
        return 0.4
