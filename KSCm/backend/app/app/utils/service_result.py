import inspect
import logging

from app.utils.app_exceptions import AppExceptionCase

logger = logging.getLogger("uvicorn.error")


class ServiceResult(object):
    def __init__(self, arg: AppExceptionCase):
        if isinstance(arg, AppExceptionCase):
            self.success = False
            self.exception_class = arg.exception_case
            self.status_code = arg.status_code
        else:
            self.success = True
            self.exception_class = None
            self.status_code = None
        self.value = arg

    def __str__(self):
        if self.success:
            return "[Success]"
        return f"[Exception] '{self.exception_class}'"

    def __repr__(self):
        if self.success:
            return "<ServiceResult Success>"
        return f"<ServiceResult AppException {self.exception_class}>"

    def __enter__(self):
        return self.value

    def __exit__(self, *kwargs):
        pass


def caller_info() -> str:
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f"{info.filename}:{info.function}:{info.lineno}"


def handle_result(result: ServiceResult):
    if not result.success:
        with result as exception:
            logger.info(f"{exception} | caller={caller_info()}")
            raise exception
    with result as result:
        return result

