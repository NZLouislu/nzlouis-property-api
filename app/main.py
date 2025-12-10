from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from datetime import datetime, timezone
from app.config import get_settings
from app.routers import properties, forecast, regions

settings = get_settings()

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="New Zealand Property Data API - Property Search, Forecast, and Regional Data",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(properties.router, prefix=settings.api_prefix)
app.include_router(forecast.router, prefix=settings.api_prefix)
app.include_router(regions.router, prefix=settings.api_prefix)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.api_version,
        "service": "nz-property-api",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=7860,
        reload=True
    )
