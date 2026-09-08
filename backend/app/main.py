print("MAIN MODULE LOADED")  # module-level boot confirmation

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api import meetings, transcripts, summary, action_items
from app.core.exceptions import NotFoundError, ValidationError
from app.db.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Modern FastAPI lifespan handler (replaces deprecated @app.on_event).
    Runs before the app starts accepting requests on every boot / redeploy.
    1. Creates all tables — idempotent (CREATE TABLE IF NOT EXISTS).
    2. Seeds demo data only if the meetings table is empty.
    """
    from app.db.session import create_tables, SessionLocal
    from app.models.meeting import Meeting

    print("[startup] Creating database tables...")
    create_tables()
    print("[startup] Tables ready.")

    db = SessionLocal()
    try:
        count = db.query(Meeting).count()
    finally:
        db.close()

    if count == 0:
        print("[startup] Database is empty — running seed loader...")
        try:
            from app.seed_loader import main as run_seed
            run_seed()
            print("[startup] Seed completed successfully.")
        except Exception as exc:
            # App still boots; it just won't have demo data
            print(f"[startup] WARNING: Seed failed — {exc}")
    else:
        print(f"[startup] Database already has {count} meeting(s) — skipping seed.")

    yield  # app runs here
    # (shutdown logic would go after yield if needed)


app = FastAPI(title="Lumen API", version="1.0.0", lifespan=lifespan)

# CORS — comma-separated CORS_ORIGINS env var; falls back to localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()],
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
