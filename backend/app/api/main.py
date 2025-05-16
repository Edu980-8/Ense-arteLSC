from fastapi import APIRouter

from app.api.routes import utils, users, auth, categories, signs, medals#items, login, private, users, utils
#from app.core.config import settings

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(categories.router)
api_router.include_router(signs.router)
api_router.include_router(medals.router)


# if settings.ENVIRONMENT == "local":
#     api_router.include_router(private.router)