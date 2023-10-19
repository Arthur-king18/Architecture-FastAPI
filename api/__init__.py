from fastapi import APIRouter

from api.user.v1.user import user_router as user_v1_router
from api.auth.auth import auth_router
from api.constants import USER_V1_API_PREFIX, AUTH_API_PREFIX

router = APIRouter()

router.include_router(user_v1_router, prefix=USER_V1_API_PREFIX, tags=["User"])
router.include_router(auth_router, prefix=AUTH_API_PREFIX, tags=["Auth"])


__all__ = ["router"]
