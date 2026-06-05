import functools
import logging
import time
import traceback

from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import serializers, status
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


def basic_exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            raise serializers.ValidationError(e.message)
        except serializers.ValidationError as e:
            if hasattr(e, 'detail'):
                raise APIException(code=e.status_code, detail=e.detail)
            raise e
        except NotImplementedError as e:
            raise APIException(code=status.HTTP_501_NOT_IMPLEMENTED, detail=str(e))
        except Exception as e:
            if settings.DEBUG:
                detail = {
                    "user message (settings.API_EXCEPTION_MESSAGE)": settings.API_EXCEPTION_MESSAGE,
                    "type": type(e),
                    "error": str(e),
                    "stacktrace": traceback.format_exc(),
                }
                print("\n",traceback.format_exc())
                raise APIException(code=500, detail=detail)
            # Don't send complex exception messages to the client when in production
            raise APIException(settings.API_EXCEPTION_MESSAGE)

    return wrapper


def log_execution_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(
            f"Function '{func.__name__}' executed in {execution_time:.4f} seconds"
        )
        return result

    if settings.DEBUG:
        return wrapper
    else:
        return func
