from fastapi import Request
from starlette.responses import JSONResponse


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: dict):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code={self.status_code} - context={self.context}"
        )


async def app_exception_handler(request: Request, exc: AppExceptionCase):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "context": exc.context,
        },
    )


class AppException(object):
    class MediaCreate(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Media creation failed
            :param context:
            """
            status_code = 500
            AppExceptionCase.__init__(self, status_code, context)

    class MediaGet(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Media not found
            :param context:
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class StoreCreate(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Store creation failed
            :param context:
            """
            status_code = 500
            AppExceptionCase.__init__(self, status_code, context)

    class StoreGet(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Store not found
            :param context:
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class StoreRequiresAuth(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Store requires auth
            :param context:
            """
            status_code = 401
            AppExceptionCase.__init__(self, status_code, context)
