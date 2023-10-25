import os
from chalice.app import CognitoUserPoolAuthorizer


def mobile_api_authorizer(authorizer_arn=os.getenv("AUTHORIZER_ARN")):
    authorizer_name = "_API_COGNITO_AUTHORIZER"

    if authorizer_arn:
        globals()[authorizer_name] = CognitoUserPoolAuthorizer(
            "DefaultCognitoAuthorizer",
            provider_arns=[authorizer_arn]
        )

    return globals().get(authorizer_name)


def get_current_user() -> dict:
    # logic to get authorized user from Lambda context
    pass
