from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .core.config import settings
from .core.database import create_tables
from .api.v1.endpoints import places, users, recommendations, maps

# Create FastAPI app
app = FastAPI(
    title="AskMyCommunity API",
    description="API for discovering amazing places in your city",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    places.router,
    prefix="/api/v1/places",
    tags=["places"]
)

app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["users"]
)

app.include_router(
    recommendations.router,
    prefix="/api/v1/recommendations",
    tags=["recommendations"]
)

app.include_router(
    maps.router,
    prefix="/api/v1/maps",
    tags=["maps"]
)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "AskMyCommunity API is running"}

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to AskMyCommunity API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    create_tables()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
