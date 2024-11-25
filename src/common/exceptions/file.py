from common.exceptions import AppException
from common.exceptions.base import ObjectAlreadyExists, ObjectDoesNotExist


class FileException(AppException):
    """Base File Exception"""


class FileAlreadyExists(ObjectAlreadyExists):
    """File Already Exists"""


class FileNotExists(ObjectDoesNotExist):
    """File Not Exists"""
