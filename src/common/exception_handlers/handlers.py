from fastapi import status

from common.exception_handlers import RequestIdJsonExceptionHandler
from common.exceptions import IntegrityDataError
from common.exceptions.base import ObjectAlreadyExists, ObjectDoesNotExist


class ValidationExceptionHandler(RequestIdJsonExceptionHandler):
    status_code = status.HTTP_400_BAD_REQUEST
    exception = IntegrityDataError


class ObjectDoesNotExistExceptionHandler(RequestIdJsonExceptionHandler):
    status_code = status.HTTP_404_NOT_FOUND
    exception = ObjectDoesNotExist


class ObjectAlreadyExistsExceptionHandler(RequestIdJsonExceptionHandler):
    status_code = status.HTTP_409_CONFLICT
    exception = ObjectAlreadyExists
