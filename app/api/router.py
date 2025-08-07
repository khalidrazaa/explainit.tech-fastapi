from fastapi import APIRouter
from app.api.admin import admin_routes
from app.api.auth import auth_routes

router = APIRouter()
router.include_router(admin_routes.router, prefix="/admin", tags=["admin"])
router.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
