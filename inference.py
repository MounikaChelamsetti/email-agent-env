import requests

BASE = "http://127.0.0.1:8000"

def log_start():
    print("[START] task=email env=email-env model=baseline", flush=True)

def log_step(step, action, reward, done, error=None):
    error_val = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}", flush=True)

def log_end(success, steps, score, rewards):
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


log_start()

obs = requests.get(f"{BASE}/reset").json()

rewards = []
done = False

for i in range(5):

    if i == 0:
        action = {"action_type": "prioritize", "email_id": 1}
    elif i == 1:
        action = {"action_type": "classify", "email_id": 2}
    else:
        action = {"action_type": "reply", "email_id": 1, "content": "Working on it"}

    res = requests.post(f"{BASE}/step", json=action).json()

    reward = res[1]
    done = res[2]

    rewards.append(reward)

    log_step(i, action["action_type"], reward, done)

    if done:
        break

final_score = sum(rewards) / len(rewards)

log_end(True, len(rewards), final_score, rewards)
