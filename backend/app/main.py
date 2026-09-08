from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api import meetings, transcripts, summary, action_items
from app.core.exceptions import NotFoundError, ValidationError
from app.db.config import settings

app = FastAPI(title="Lumen API", version="1.0.0")

# CORS — origins come from CORS_ORIGINS env var (comma-separated), with localhost:3000 as dev fallback
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Exception Handlers
@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": "NOT_FOUND", "message": exc.message}
    )

@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "VALIDATION_ERROR", "message": exc.message}
    )

# Include Routers
app.include_router(meetings.router, prefix="/api")
app.include_router(transcripts.router, prefix="/api")
app.include_router(summary.router, prefix="/api")
app.include_router(action_items.router, prefix="/api")

@app.get("/api/health", tags=["health"])
def health_check():
    return {"status": "ok"}
