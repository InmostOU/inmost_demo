from typing import Dict, Optional

from chalice import Response, CORSConfig

from ... import logger
from . import errors


def response_error(error: errors.BaseErrorX, headers: Optional[Dict[str, str]] = None):
    if headers is None:
        headers = {}

    error_message = error.message
    code = error.status_code
    error_title = error.error_title

    response = {
        "success": False,
        "error": error_title,
        "message": error_message,
    }

    cors_config = CORSConfig(allow_origin="*")
    headers.update(cors_config.get_access_control_headers())
    response = Response(
        status_code=code,
        body=response,
        headers=headers
    )

    logger.Logger.error(f"ErrorResponse: {response.to_dict()}")

    return response


def response_success(body, code=200, pagination=None, headers: Optional[Dict[str, str]] = None):
    response = {
        "success": True,
        "data": body
    }
    if pagination:
        response["pagination"] = pagination

    response = Response(
        status_code=code,
        body=response,
        headers=headers
    )

    logger.Logger.info(f"SuccessResponse: {response.to_dict()}")

    return response
