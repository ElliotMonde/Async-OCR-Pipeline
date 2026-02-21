from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.ocr_router import router as ocr_router
from api.routers.image_sync_router import router as image_sync_router
from shared.core.exceptions import APIException
from fastapi.responses import JSONResponse
from fastapi import Request
from shared.db.database import engine, wait_for_db
from shared.db.models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    await wait_for_db()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Database tables created.")
    yield


app = FastAPI(title="Image OCR Service", lifespan=lifespan)
    

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
)

app.include_router(ocr_router)
app.include_router(image_sync_router)


@app.exception_handler(APIException)
def unicorn_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.get("/")
def read_root():
    return "Image OCR service is running.To use this API, please visit /docs"
