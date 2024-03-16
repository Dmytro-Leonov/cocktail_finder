from app.core.exceptions import NotAuthenticated, PermissionDenied
from app.modules.auth.constants import ErrorCode


class AuthorizationFailed(PermissionDenied):
    DETAIL = ErrorCode.AUTHORIZATION_FAILED


class InvalidToken(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_TOKEN


class InvalidCredentials(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_CREDENTIALS
