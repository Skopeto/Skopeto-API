import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.routes import auth, servers
from app.core.Exception import AppBaseException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI()

@app.exception_handler(AppBaseException)
async def app_exception_handler(request: Request, exc: AppBaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )

app.include_router(auth.router)
app.include_router(servers.router)

@app.get("/")
def root():
    return {"status": "ok"}
