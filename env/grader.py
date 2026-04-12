"""
Graders for the email-agent-env.
All scores are strictly between 0.0 and 1.0 (exclusive).
"""
from typing import Any, Dict, List


def _clamp(score: float) -> float:
	return max(0.001, min(0.999, float(score)))


def grade(actions: List[Dict[str, Any]]) -> float:
	"""Legacy grader used by inference.py - do not remove."""
	if not actions:
		return 0.001
	action_types = {a.get("action_type") for a in actions}
	score = 0.0
	if "prioritize" in action_types:
		score += 0.4
	if "classify" in action_types:
		score += 0.3
	if "reply" in action_types:
		score += 0.2
	return _clamp(score)


def grade_easy(state: Dict[str, Any]) -> float:
	"""Easy task: prioritize the urgent email."""
	try:
		actions = state.get("actions", [])
		emails = state.get("emails", [])
		urgent_ids = {e["id"] for e in emails if e.get("is_urgent")}
		prioritized_ids = {
			a["email_id"] for a in actions
			if a.get("action_type") == "prioritize"
		}
		if not urgent_ids:
			has_any = any(a.get("action_type") == "prioritize" for a in actions)
			return _clamp(0.6 if has_any else 0.1)
		ratio = len(urgent_ids & prioritized_ids) / len(urgent_ids)
		return _clamp(0.05 + ratio * 0.944)
	except Exception:
		return 0.001


def grade_medium(state: Dict[str, Any]) -> float:
	"""Medium task: classify spam correctly."""
	try:
		actions = state.get("actions", [])
		emails = state.get("emails", [])
		spam_ids = {e["id"] for e in emails if e.get("is_spam")}
		classified_spam = {
			a["email_id"] for a in actions
			if a.get("action_type") == "classify" and a.get("label") == "spam"
		}
		if not spam_ids:
			has_any = any(a.get("action_type") == "classify" for a in actions)
			return _clamp(0.6 if has_any else 0.1)
		tp = len(spam_ids & classified_spam)
		fp = len(classified_spam - spam_ids)
		fn = len(spam_ids - classified_spam)
		precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
		recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
		f1 = (2 * precision * recall / (precision + recall)
			  if (precision + recall) > 0 else 0.0)
		return _clamp(0.05 + f1 * 0.949)
	except Exception:
		return 0.001


def grade_hard(state: Dict[str, Any]) -> float:
	"""Hard task: prioritize urgent, classify spam, reply to normal emails."""
	try:
		actions = state.get("actions", [])
		emails = state.get("emails", [])
		urgent_ids = {e["id"] for e in emails if e.get("is_urgent")}
		spam_ids = {e["id"] for e in emails if e.get("is_spam")}
		normal_ids = {e["id"] for e in emails
					  if not e.get("is_urgent") and not e.get("is_spam")}
		prioritized = {a["email_id"] for a in actions
					   if a.get("action_type") == "prioritize"}
		classified_sp = {a["email_id"] for a in actions
						 if a.get("action_type") == "classify"
						 and a.get("label") == "spam"}
		replied = {a["email_id"] for a in actions
				   if a.get("action_type") == "reply"}
		urgent_score = (len(urgent_ids & prioritized) / len(urgent_ids)
						if urgent_ids else 0.5)
		spam_score = (len(spam_ids & classified_sp) / len(spam_ids)
					  if spam_ids else 0.5)
		reply_score = (len(normal_ids & replied) / len(normal_ids)
					   if normal_ids else 0.5)
		combined = 0.4 * urgent_score + 0.3 * spam_score + 0.3 * reply_score
		return _clamp(combined)
	except Exception:
		return 0.001
