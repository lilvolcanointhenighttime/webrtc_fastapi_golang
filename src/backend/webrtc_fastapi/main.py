import uvicorn

from .app import get_app

app = get_app()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, workers=1, log_level='debug', access_log=True)