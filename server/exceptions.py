from django.core import exceptions as django_exceptions


class ServerException(Exception):
    """Base class for all exceptions"""

    default_message = "Internal server error"

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super().__init__(message)


class PermissionDenied(ServerException, django_exceptions.PermissionDenied):
    default_message = "You do not have permission to perform this action"
