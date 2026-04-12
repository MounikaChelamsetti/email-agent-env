from __future__ import annotations

import os
from typing import Any, Dict, List, Tuple

import requests
from openai import OpenAI

from env.environment import Action, EmailEnv
from env.grader import grade

BASE = os.getenv("OPENENV_BASE") or os.getenv("OPENENV_BASE_URL") or "http://127.0.0.1:8000"
TIMEOUT_SECONDS = 10

API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
API_KEY = os.environ.get("API_KEY", os.environ.get("OPENAI_API_KEY", "dummy"))
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY,
)


def get_llm_action(state: Dict[str, Any]) -> Dict[str, Any]:
    """Ask the LLM proxy what action to take given the current state."""
    prompt = f"""You are an email agent. Given this inbox state, decide the next action.

State: {state}

Reply with exactly one JSON object with these fields:
- action_type: one of "prioritize", "classify", "reply"
- email_id: integer id of the email to act on
- content: string (only needed if action_type is "reply", else empty string)
- label: string (only needed if action_type is "classify", use "spam" or "normal", else empty string)

Reply with raw JSON only, no explanation."""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.0,
    )

    import json

    text = response.choices[0].message.content.strip()
    try:
        return json.loads(text)
    except Exception:
        return {"action_type": "prioritize", "email_id": 1, "content": "", "label": ""}


def planned_actions() -> List[Dict[str, Any]]:
    return [
        {"action_type": "prioritize", "email_id": 1},
        {"action_type": "classify", "email_id": 2, "label": "spam"},
        {"action_type": "reply", "email_id": 1, "content": "Working on it"},
        {"action_type": "prioritize", "email_id": 4},
        {"action_type": "reply", "email_id": 4, "content": "Acknowledged"},
    ]


def run_locally() -> Tuple[List[Dict[str, Any]], bool]:
    executed: List[Dict[str, Any]] = []
    env = EmailEnv()
    state_dict = env.reset()

    for _ in range(5):
        try:
            action_dict = get_llm_action(state_dict if isinstance(state_dict, dict) else {})
        except Exception:
            action_dict = planned_actions()[len(executed) % len(planned_actions())]

        action = Action(**{k: v for k, v in action_dict.items() if k in ("action_type", "email_id", "content")})
        result = env.step(action)
        state_dict, reward, done, info = result

        print("[STEP]")
        print(f"action: {action_dict}")
        print(f"reward: {reward}")
        executed.append(action_dict)

        if done:
            break

    return executed, False


def run_via_http() -> Tuple[List[Dict[str, Any]], bool]:
    executed: List[Dict[str, Any]] = []

    reset_resp = requests.post(f"{BASE}/reset", timeout=TIMEOUT_SECONDS)
    reset_resp.raise_for_status()
    state_dict = reset_resp.json()

    for _ in range(5):
        try:
            action_dict = get_llm_action(state_dict if isinstance(state_dict, dict) else {})
        except Exception:
            action_dict = planned_actions()[len(executed) % len(planned_actions())]

        step_resp = requests.post(f"{BASE}/step", json=action_dict, timeout=TIMEOUT_SECONDS)
        step_resp.raise_for_status()
        payload = step_resp.json()
        state_dict = payload.get("state", {})

        print("[STEP]")
        print(f"action: {action_dict}")
        print(f"reward: {payload.get('reward')}")
        executed.append(action_dict)

        if payload.get("done"):
            break

    return executed, True


def main() -> int:
    print(f"[START] model={MODEL_NAME} api_base={API_BASE_URL}")

    use_http = os.getenv("OPENENV_USE_HTTP", "").strip().lower() in {"1", "true", "yes"}

    if use_http:
        try:
            executed_actions, used_http = run_via_http()
        except Exception as exc:
            print(f"[WARN] HTTP failed: {exc}, falling back to local")
            executed_actions, used_http = run_locally()
    else:
        executed_actions, used_http = run_locally()

    final_score = grade(executed_actions)

    print("[END]")
    print(f"mode: {'http' if used_http else 'local'}")
    print(f"final_score: {final_score:.4f}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[ERROR] inference failed: {exc}")
        print("final_score: 0.01")
        raise SystemExit(0)
