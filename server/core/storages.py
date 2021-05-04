from django.conf import settings
from django.core.files.storage import FileSystemStorage

from storages.backends.s3boto3 import S3Boto3Storage


class AWSPrivateStorage(S3Boto3Storage):
    default_acl = "private"
    file_overwrite = False
    custom_domain = False


def get_private_storage(location):
    if settings.USE_S3:
        return AWSPrivateStorage(location=location)
    else:
        return FileSystemStorage()
