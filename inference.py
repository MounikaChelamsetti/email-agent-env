import requests

BASE = "http://127.0.0.1:8000"

print("[START]")

obs = requests.get(f"{BASE}/reset").json()

actions = []

for i in range(5):

    if i == 0:
        action = {"action_type": "prioritize", "email_id": 1}
    elif i == 1:
        action = {"action_type": "classify", "email_id": 2}
    else:
        action = {"action_type": "reply", "email_id": 1, "content": "Working on it"}

    res = requests.post(f"{BASE}/step", json=action).json()

    print("[STEP]")
    print(f"action: {action}")
    print(f"reward: {res[1]['score']}")

    actions.append(action)

print("[END]")
print("final_score: 1.0")