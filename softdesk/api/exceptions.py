from rest_framework.exceptions import PermissionDenied
from rest_framework import status


class UserNotInProject(PermissionDenied):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "This user doesn't work on this project"
    default_code = 'Not found'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code

class UserAlreadyInProject(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "This user already work on this project"
    default_code = 'Conflict'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code
