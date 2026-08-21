# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Query
# pyrefly: ignore [missing-import]
from fastapi.testclient import TestClient

app = FastAPI()

@app.post("/trigger")
def trigger(repo_name: str = Query(...)):
    print("Received repo_name:", repo_name)
    return {"repo_name": repo_name}

client = TestClient(app)
client.post("/trigger?repo_name=ashwini-coder11%2Fai-code-review-test")
