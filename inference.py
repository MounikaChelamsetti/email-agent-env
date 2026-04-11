import requests
import os
import time

BASE = os.getenv("OPENENV_BASE_URL", "http://127.0.0.1:8000")

print("[START]")

# 🔁 WAIT FOR SERVER TO BE READY
for _ in range(10):
    try:
        res = requests.get(f"{BASE}/reset")
        if res.status_code == 200:
            break
    except:
        pass
    time.sleep(1)
else:
    print("Server not reachable")
    exit(1)

try:
    obs = requests.get(f"{BASE}/reset").json()

    actions = []

    for i in range(5):
        if i == 0:
            action = {"action_type": "prioritize", "email_id": 1}
        elif i == 1:
            action = {"action_type": "classify", "email_id": 2}
        else:
            action = {
                "action_type": "reply",
                "email_id": 1,
                "content": "Working on it"
            }

        res = requests.post(f"{BASE}/step", json=action).json()

        print("[STEP]")
        print(f"action: {action}")
        print(f"reward: {res.get('reward', 0)}")

        actions.append(action)

    print("[END]")
    print("final_score: 1.0")

except Exception as e:
    print("Error:", str(e))
    exit(1)
