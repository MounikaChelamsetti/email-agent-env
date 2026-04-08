from fastapi import FastAPI
from env.environment import EmailEnv, Action

app = FastAPI()
env = EmailEnv()

@app.get("/")
def home():
    return {"message": "Running"}


@app.post("/reset")
def reset():
    return env.reset()

@app.get("/reset")
def reset_get():
    return env.reset()

@app.post("/step")
def step(action: Action):
    state, reward, done, info = env.step(action)

    return {
        "state": state,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()
