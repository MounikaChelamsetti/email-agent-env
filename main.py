from fastapi import FastAPI
from env.environment import EmailEnv, Action

app = FastAPI()
env = EmailEnv()

@app.get("/")
def home():
    return {"message": "Running"}

@app.get("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: Action):
    return env.step(action)

@app.get("/state")
def state():
    return env.state()