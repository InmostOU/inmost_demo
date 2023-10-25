from chalice.app import Request

from .libs import models
from src.profile.chalicelib.libs.utils.authorize_util import get_current_user
from .libs.utils import errors, messages
from .libs.utils.response_handler import response_success


def get_profile(request: Request):
    """
        GET /user
    """
    user = get_current_user()
    return response_success(user)


def update_profile(request: Request):
    """
        PUT /user
    """
    user = get_current_user()
    update_body = request.json_body
    if not update_body:
        raise errors.BadRequestErrorX(messages.MISSING_BODY_IN_REQUEST)

    updated_user = models.UserModel.update_by_id(
        id=user["id"],
        update_body=update_body
    )

    return response_success(updated_user)
