import json
import http
from typing import Any, Dict, List, Union, Tuple


class BaseErrorX(BaseException):
    def __init__(self, message, status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR, error_title=None) -> None:
        self.error_title = error_title if error_title else self.__class__.__name__
        self.message = message
        self.status_code = status_code

    def to_dict(self) -> Dict[Any, Any]:
        # Don't copy internal attributes.
        copied = {
            k: v for k, v in self.__dict__.items()
            if not k.startswith('_')
        }
        return copied

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class ValidationErrorX(BaseErrorX):
    def __init__(self, messages: Union[List[str], Tuple[str, str], str], json_path) -> None:
        debug_message = messages if isinstance(messages, str) else messages[0]
        pretty_message = messages[1] if len(messages) > 1 else debug_message
        super().__init__(pretty_message, http.HTTPStatus.UNPROCESSABLE_ENTITY)
        self.debug_message = debug_message
        self.json_path = json_path


class BadRequestErrorX(BaseErrorX):
    def __init__(self, message) -> None:
        super().__init__(message,  http.HTTPStatus.BAD_REQUEST)


class InvalidTokenErrorX(BaseErrorX):
    def __init__(self, message) -> None:
        super().__init__(message,  http.HTTPStatus.BAD_REQUEST)


class ObjectExistsErrorX(BaseErrorX):
    def __init__(self, message) -> None:
        super().__init__(message, http.HTTPStatus.INTERNAL_SERVER_ERROR)


class NotFoundErrorX(BaseErrorX):
    def __init__(self, message) -> None:
        super().__init__(message, http.HTTPStatus.NOT_FOUND)


class NotAuthorizedErrorX(BaseErrorX):
    def __init__(self, message) -> None:
        super().__init__(message, http.HTTPStatus.UNAUTHORIZED)


class ForbiddenErrorX(BaseErrorX):
    def __init__(self, message) -> None:
        super().__init__(message, http.HTTPStatus.FORBIDDEN)


class OutdatedDataErrorX(BaseErrorX):
    def __init__(self, message) -> None:
        super().__init__(message,  http.HTTPStatus.BAD_REQUEST)


class UpdateErrorX(BaseErrorX):
    def __init__(self, message) -> None:
        super().__init__(message, http.HTTPStatus.BAD_REQUEST)


class DeletionErrorX(BaseErrorX):
    def __init__(self, message) -> None:
        super().__init__(message, http.HTTPStatus.BAD_REQUEST)


class InvalidInputErrorX(BaseErrorX):
    def __init__(self, message) -> None:
        super().__init__(message, http.HTTPStatus.UNPROCESSABLE_ENTITY)


class NoContentErrorX(BaseErrorX):
    def __init__(self, message) -> None:
        super().__init__(message, http.HTTPStatus.NO_CONTENT)
