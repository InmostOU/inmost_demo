from .authorization_handler import handle_cognito_auth, handle_supporters_cognito_auth
from .error_handler import handle_errors, handle_pure_lambdas_errors
from .request_data_handler import handle_request_data

from aws_xray_sdk.core import patch_all, xray_recorder

xray_recorder.configure(context_missing="IGNORE_ERROR", stream_sql=True)
patch_all()
