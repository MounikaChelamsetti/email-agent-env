
# 📧 Email Agent Environment (OpenEnv)

A **real-world AI environment** for simulating email inbox management tasks such as prioritization, spam detection, and automated replies.

Built for **agent training, evaluation, and benchmarking** in realistic scenarios.

---

## 🎯 Motivation

Managing emails is a complex real-world problem involving:

- Time-sensitive decision making  
- Multi-step reasoning  
- Prioritization under constraints  
- Natural language understanding  

This environment enables agents to learn **practical inbox workflows**, making it useful for:

- Autonomous AI assistants  
- Productivity tools  
- Reinforcement Learning benchmarking  

---

## 🌍 Real-World Impact

Email overload affects millions of users daily.

This environment helps:

- Train AI-powered email assistants  
- Automate repetitive inbox tasks  
- Improve productivity systems  
- Benchmark decision-making agents  

It bridges the gap between **toy environments and real-world applications**.

---

## 🧠 Environment Overview

The agent interacts with an inbox and must:

1. Identify urgent emails  
2. Classify spam vs normal  
3. Respond appropriately  
4. Minimize unnecessary actions  

---

##   📊 Evaluation Metrics

Agent performance is evaluated using a score between 0.0 and 1.0 based on:

Accuracy of prioritization (urgent emails handled correctly)
Correct spam classification
Quality and relevance of generated replies
Efficiency (fewer steps → higher score)

Final Score = weighted combination of all factors

✔ Deterministic evaluation
✔ Reproducible results
✔ Fair comparison across agents


##   🧩 Task Details with Examples
🟢 Easy Task

Input:

"Submit report by 6pm or escalation"

Expected Behavior:

Identify as urgent
Prioritize correctly
🟡 Medium Task

Input:

"Win $5000 now!!!"

Expected Behavior:

Classify as spam
Avoid false positives
🔴 Hard Task

Input:

Mixed inbox with multiple emails

Example:

"Submit report by 6pm"
"Win lottery now!!!"
"Meeting at 11am"

Expected Behavior:

Prioritize urgent emails
Ignore spam
Respond appropriately
Maintain efficient action sequence
##   🔁 Determinism & Reproducibility
Fully deterministic environment
Same input → same output
No randomness in rewards
Stable benchmarking

Ensures:

Reliable evaluation
Fair model comparison
Consistent agent performance
##   🌍 Why This Matters

This project simulates real-world decision-making scenarios, unlike toy environments.

It enables:

Practical AI deployment
Multi-step reasoning evaluation
Realistic agent benchmarking
##🚀 API Endpoints
Endpoint	Description
/reset	Reset environment
/step	Perform action
/state	Get current state
##   🧪 Example Usage
curl -X POST "https://your-space-url/step" \
-H "Content-Type: application/json" \
-d '{
  "action_type": "prioritize",
  "email_id": 1,
  "content": ""
}'
##    ⚙️ Run Locally
pip install -r requirements.txt
uvicorn main:app --reload
##   🏗️ Tech Stack
FastAPI
Python
Docker
Hugging Face Spaces
##   🏁 Conclusion

This project provides a realistic environment for training AI agents on inbox management tasks, combining:

Decision-making
NLP understanding
Multi-step reasoning

## ⚙️ Action Space

```json
{
  "action_type": "classify | prioritize | reply",
  "email_id": int,
  "content": "optional reply text"
}
