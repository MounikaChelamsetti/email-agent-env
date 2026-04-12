def grade_easy(state, trajectory):
    """Grade easy task: handling a normal email."""
    score = 0.5  # base score

    history = getattr(state, "history", []) or []
    emails = getattr(state, "emails", []) or []

    if not history:
        return 0.1  # agent did nothing — low but not zero

    # Reward for acting on normal emails
    actions_taken = len(history)
    score += min(0.3, actions_taken * 0.1)

    # Check if normal emails were handled
    normal_emails = [e for e in emails if getattr(e, "type", None) == "normal"]
    if normal_emails:
        score += 0.1

    return max(0.001, min(0.999, score))


def grade_medium(state, trajectory):
    """Grade medium task: handling urgent emails correctly."""
    score = 0.4

    history = getattr(state, "history", []) or []
    emails = getattr(state, "emails", []) or []

    if not history:
        return 0.15

    urgent_emails = [e for e in emails if getattr(e, "type", None) == "urgent"]
    if urgent_emails and len(history) >= len(urgent_emails):
        score += 0.35

    actions_taken = len(history)
    score += min(0.2, actions_taken * 0.05)

    return max(0.001, min(0.999, score))


def grade_hard(state, trajectory):
    """Grade hard task: spam detection and classification."""
    score = 0.3

    history = getattr(state, "history", []) or []
    emails = getattr(state, "emails", []) or []

    if not history:
        return 0.2

    spam_emails = [e for e in emails if getattr(e, "type", None) == "spam"]
    if spam_emails and len(history) > 0:
        score += 0.4

    # Bonus for multi-step handling
    if len(history) >= 3:
        score += 0.2

    return max(0.001, min(0.999, score))
