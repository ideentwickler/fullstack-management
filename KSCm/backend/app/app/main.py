from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.utils.app_exceptions import AppExceptionCase, app_exception_handler
from app.api.api_v1.api import api_router
from app.views.views import view_router
from app.core.config import settings

from app.utils.request_exceptions import \
    http_exception_handler,\
    request_validation_exception_handler

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


# https://github.com/visini/abstracting-fastapi-services
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Api Router: /api/...
app.include_router(api_router, prefix=settings.API_V1_STR)
# View Router: /views/...
app.include_router(view_router, prefix=settings.APP_VIEW_STR)
