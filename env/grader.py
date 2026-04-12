from typing import Any, Dict, List


def _clamp(score: float) -> float:
    return max(0.001, min(0.999, float(score)))


def _get_actions(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    actions = state.get("actions") or state.get("history") or []
    return [a for a in actions if isinstance(a, dict)]


def _get_emails(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    emails = state.get("emails") or []
    return [e for e in emails if isinstance(e, dict)]


def grade(actions, trajectory=None):
    """Legacy function required by inference.py"""
    if not actions:
        return _clamp(0.5)
    if isinstance(actions, dict):
        actions = _get_actions(actions)
    action_types = {a.get("action_type") for a in actions if isinstance(a, dict)}
    score = 0.1
    if "prioritize" in action_types:
        score += 0.4
    if "classify" in action_types:
        score += 0.3
    if "reply" in action_types:
        score += 0.2
    return _clamp(score)


def grade_easy(state: Dict[str, Any]) -> float:
    try:
        actions = _get_actions(state)
        emails = _get_emails(state)

        urgent_ids = {e["id"] for e in emails if e.get("is_urgent")}
        prioritized_ids = {
            a["email_id"] for a in actions
            if a.get("action_type") == "prioritize" and "email_id" in a
        }

        if not emails:
            return _clamp(0.5)

        if not urgent_ids:
            return _clamp(0.6 if prioritized_ids else 0.2)

        ratio = len(urgent_ids & prioritized_ids) / len(urgent_ids)
        return _clamp(0.05 + ratio * 0.944)
    except Exception:
        return _clamp(0.5)


def grade_medium(state: Dict[str, Any]) -> float:
    try:
        actions = _get_actions(state)
        emails = _get_emails(state)

        spam_ids = {e["id"] for e in emails if e.get("is_spam")}
        classified_spam = {
            a["email_id"] for a in actions
            if a.get("action_type") == "classify" and a.get("label") == "spam"
            and "email_id" in a
        }

        if not emails:
            return _clamp(0.5)

        if not spam_ids:
            return _clamp(0.6 if classified_spam else 0.2)

        tp = len(spam_ids & classified_spam)
        fp = len(classified_spam - spam_ids)
        fn = len(spam_ids - classified_spam)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)
              if (precision + recall) > 0 else 0.0)
        return _clamp(0.05 + f1 * 0.949)
    except Exception:
        return _clamp(0.5)


def grade_hard(state: Dict[str, Any]) -> float:
    try:
        actions = _get_actions(state)
        emails = _get_emails(state)

        if not emails:
            return _clamp(0.5)

        urgent_ids = {e["id"] for e in emails if e.get("is_urgent")}
        spam_ids = {e["id"] for e in emails if e.get("is_spam")}
        normal_ids = {
            e["id"] for e in emails
            if not e.get("is_urgent") and not e.get("is_spam")
        }

        prioritized = {
            a["email_id"] for a in actions
            if a.get("action_type") == "prioritize" and "email_id" in a
        }
        classified_sp = {
            a["email_id"] for a in actions
            if a.get("action_type") == "classify"
            and a.get("label") == "spam" and "email_id" in a
        }
        replied = {
            a["email_id"] for a in actions
            if a.get("action_type") == "reply" and "email_id" in a
        }

        urgent_score = (len(urgent_ids & prioritized) / len(urgent_ids)
                        if urgent_ids else 0.5)
        spam_score = (len(spam_ids & classified_sp) / len(spam_ids)
                      if spam_ids else 0.5)
        reply_score = (len(normal_ids & replied) / len(normal_ids)
                       if normal_ids else 0.5)

        raw = 0.4 * urgent_score + 0.3 * spam_score + 0.3 * reply_score
        return _clamp(raw)
    except Exception:
        return _clamp(0.5)
