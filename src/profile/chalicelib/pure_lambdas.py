from .libs import models
from .libs.utils import messages, errors


def signup_validation(event, context):
    cognito_username = event["userName"]
    user = models.UserModel.get_by_cognito_username(cognito_username)

    if user and user.get("active"):
        raise errors.ObjectExistsErrorX(messages.COGNITO_USERNAME_EXISTS)

    return event
