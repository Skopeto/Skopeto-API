from fastapi import FastAPI
from app.api.routes import auth, servers

app = FastAPI()

app.include_router(auth.router)
app.include_router(servers.router)

@app.get("/")
def root():
    return {"status": "ok"}
