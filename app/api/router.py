from fastapi import APIRouter
from app.api.admin import routes as admin_routes
from app.api.auth import routes as auth_routes

router = APIRouter()
router.include_router(admin_routes.router, prefix="/admin", tags=["admin"])
router.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
