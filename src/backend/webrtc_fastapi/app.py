
import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import webrtc_router
from .utils import pc_dict



@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    coros = [pc.close() for _, pc in pc_dict.items()]
    await asyncio.gather(*coros)
    pc_dict.clear()



def get_app() -> FastAPI:
    app = FastAPI(title="WebRTC", lifespan=lifespan, root_path="/api/v1")

    origins = ["*"]
    app.add_middleware(
        CORSMiddleware, 
        allow_origins=origins,
        allow_credentials=True, 
        allow_methods=['*'], 
        allow_headers=['*'])

    app.include_router(webrtc_router)
    return app

app = get_app()



