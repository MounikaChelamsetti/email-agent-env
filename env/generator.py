def generate_emails():
    return [
        {"id": 1, "subject": "URGENT: Server down", "type": "urgent",
         "is_urgent": True, "is_spam": False},
        {"id": 2, "subject": "You won a prize!", "type": "spam",
         "is_urgent": False, "is_spam": True},
        {"id": 3, "subject": "Team lunch tomorrow", "type": "normal",
         "is_urgent": False, "is_spam": False},
        {"id": 4, "subject": "URGENT: Client meeting", "type": "urgent",
         "is_urgent": True, "is_spam": False},
        {"id": 5, "subject": "Newsletter", "type": "spam",
         "is_urgent": False, "is_spam": True},
    ]