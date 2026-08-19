from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.routes import health, chat, search, summary, tourism_routes

app = FastAPI(
    title="Angkor Verse AI API",
    description="Intelligent Angkor Verse AI Tourism Information Service specialized in Cambodia tourism.",
    version="1.0.0",
    debug=settings.DEBUG
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers under /api prefix
app.include_router(health.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(summary.router, prefix="/api")
app.include_router(tourism_routes.router, prefix="/api")

# Also include directly without /api prefix for maximum frontend compatibility
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(search.router)
app.include_router(summary.router)
app.include_router(tourism_routes.router)

@app.on_event("startup")
def startup_event():
    try:
        from app.services.matching_service import matching_service
        matching_service.index_datasets()
        print("✅ Pre-indexed similarity dataset successfully on server startup.")
    except Exception as e:
        print(f"Startup indexing note: {e}")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": str(exc)}
    )

@app.get("/")
async def root():
    return {
        "message": "Angkor Verse AI API is running",
        "docs": "/docs",
        "health": "/api/health"
    }
