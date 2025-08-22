from fastapi import APIRouter
from app.api.api_v1.endpoints import recommendations, places, events

api_router = APIRouter()

api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(places.router, prefix="/places", tags=["places"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
