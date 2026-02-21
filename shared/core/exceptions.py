from fastapi.exceptions import HTTPException
from shared.core.error_codes import ErrorCodes


class APIException(HTTPException):
    def __init__(self, status_code: ErrorCodes, detail: str = "") -> None:
        super().__init__(status_code=status_code.value["code"], detail=detail)


class NotFoundException(APIException):
    def __init__(self, detail: str = ErrorCodes.NOT_FOUND.value["message"]) -> None:
        super().__init__(status_code=ErrorCodes.NOT_FOUND, detail=detail)


class ConflictException(APIException):
    def __init__(self, detail: str = ErrorCodes.CONFLICT.value["message"]) -> None:
        super().__init__(status_code=ErrorCodes.CONFLICT, detail=detail)


class BadRequestException(APIException):
    def __init__(self, detail: str = ErrorCodes.BAD_REQUEST.value["message"]) -> None:
        super().__init__(status_code=ErrorCodes.BAD_REQUEST, detail=detail)


class UnauthorizedException(APIException):
    def __init__(self, detail: str = ErrorCodes.UNAUTHORIZED.value["message"]) -> None:
        super().__init__(status_code=ErrorCodes.UNAUTHORIZED, detail=detail)


class ForbiddenException(APIException):
    def __init__(self, detail: str = ErrorCodes.FORBIDDEN.value["message"]) -> None:
        super().__init__(status_code=ErrorCodes.FORBIDDEN, detail=detail)


class NotImplementedException(APIException):
    def __init__(
        self, detail: str = ErrorCodes.NOT_IMPLEMENTED.value["message"]
    ) -> None:
        super().__init__(status_code=ErrorCodes.NOT_IMPLEMENTED, detail=detail)


class InternalServerErrorException(APIException):
    def __init__(
        self, detail: str = ErrorCodes.INTERNAL_SERVER_ERROR.value["message"]
    ) -> None:
        super().__init__(status_code=ErrorCodes.INTERNAL_SERVER_ERROR, detail=detail)


class ServiceUnavailableException(APIException):
    def __init__(
        self, detail: str = ErrorCodes.SERVICE_UNAVAILABLE.value["message"]
    ) -> None:
        super().__init__(status_code=ErrorCodes.SERVICE_UNAVAILABLE, detail=detail)
