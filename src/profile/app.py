from aws_xray_sdk.core import patch_all, xray_recorder
from chalice import Chalice

from chalicelib import pure_lambdas as pures, routing_lambdas as routes
from src.profile.chalicelib import logger
from src.profile.chalicelib.libs.middlewares import handle_errors

# APIGateway url_prefix for CustomDomain - /profile
app = Chalice(app_name="restapi_profile")

xray_recorder.configure(context_missing="IGNORE_ERROR")
patch_all()


@app.middleware("all")
def xray_middleware(event, get_response):
    with xray_recorder.capture('ChaliceRequest'):
        return get_response(event)


app.register_middleware(handle_errors, "http")

app.api.cors = True
app.log = logger.Logger


@app.route("/user", methods=["GET"], authorizer=helper.mobile_api_authorizer())
def get_profile():
    return routes.get_profile(app.current_request)


@app.route("/user", methods=["PUT"], authorizer=helper.mobile_api_authorizer())
def update_profile():
    return routes.update_profile(app.current_request)


@app.lambda_function()
def signup_validation(event, context):
    return pures.signup_validation(event, context)
