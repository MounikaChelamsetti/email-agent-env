from typing import Any, Dict, List


def _clamp(score: float) -> float:
    return max(0.001, min(0.999, float(score)))


# ✅ EASY
def grade_easy(state: Dict[str, Any], trajectory: List[Dict[str, Any]]) -> float:
    try:
        actions = trajectory or state.get("history", [])
        emails = state.get("emails", [])

        urgent_ids = {e["id"] for e in emails if e.get("type") == "urgent"}
        prioritized_ids = {
            a.get("email_id")
            for a in actions
            if a.get("action_type") == "prioritize"
        }

        if not urgent_ids:
            return 0.6

        ratio = len(urgent_ids & prioritized_ids) / len(urgent_ids)
        return _clamp(0.1 + ratio * 0.8)

    except Exception:
        return 0.2


# ✅ MEDIUM
def grade_medium(state: Dict[str, Any], trajectory: List[Dict[str, Any]]) -> float:
    try:
        actions = trajectory or state.get("history", [])
        emails = state.get("emails", [])

        spam_ids = {e["id"] for e in emails if e.get("type") == "spam"}
        classified_ids = {
            a.get("email_id")
            for a in actions
            if a.get("action_type") == "classify"
        }

        if not spam_ids:
            return 0.6

        ratio = len(spam_ids & classified_ids) / len(spam_ids)
        return _clamp(0.1 + ratio * 0.8)

    except Exception:
        return 0.2


# ✅ HARD
def grade_hard(state: Dict[str, Any], trajectory: List[Dict[str, Any]]) -> float:
    try:
        actions = trajectory or state.get("history", [])
        emails = state.get("emails", [])

        urgent_ids = {e["id"] for e in emails if e.get("type") == "urgent"}
        spam_ids = {e["id"] for e in emails if e.get("type") == "spam"}
        normal_ids = {e["id"] for e in emails if e.get("type") == "normal"}

        prioritized = {
            a.get("email_id")
            for a in actions
            if a.get("action_type") == "prioritize"
        }

        classified = {
            a.get("email_id")
            for a in actions
            if a.get("action_type") == "classify"
        }

        replied = {
            a.get("email_id")
            for a in actions
            if a.get("action_type") == "reply"
        }

        urgent_score = len(urgent_ids & prioritized) / len(urgent_ids) if urgent_ids else 0.5
        spam_score = len(spam_ids & classified) / len(spam_ids) if spam_ids else 0.5
        reply_score = len(normal_ids & replied) / len(normal_ids) if normal_ids else 0.5

        final_score = 0.4 * urgent_score + 0.3 * spam_score + 0.3 * reply_score

        return _clamp(final_score)

    except Exception:
        return 0.2
