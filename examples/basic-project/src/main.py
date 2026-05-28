from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
users = {"demo@example.com": "secret"}


class Credentials(BaseModel):
    email: str
    password: str


@app.post("/login")
def login(credentials: Credentials) -> dict[str, str]:
    if users.get(credentials.email) != credentials.password:
        raise HTTPException(status_code=401, detail="invalid credentials")
    return {"status": "ok"}


@app.post("/register")
def register(credentials: Credentials) -> dict[str, str]:
    users[credentials.email] = credentials.password
    return {"status": "created"}
