from .user import router as user_router
from .admin import router as admin_router


def setup_routers(dp):
    dp.include_router(user_router)
    dp.include_router(admin_router)
