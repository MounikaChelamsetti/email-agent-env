def grade(actions):
    score = 0

    for a in actions:
        if a["action_type"] == "classify":
            score += 0.3
        if a["action_type"] == "prioritize":
            score += 0.3
        if a["action_type"] == "reply":
            score += 0.4

    return min(score, 1.0)
