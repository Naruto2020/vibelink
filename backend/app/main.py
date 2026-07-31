from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Vibelink API is running" }
