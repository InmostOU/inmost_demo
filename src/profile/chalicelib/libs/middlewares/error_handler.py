from pw_lambda_lib.logger import Logger
from pw_lambda_lib.utils import errors, response_handler


def handle_errors(event, get_response):
    """
        event is of type chalice.app.Request or lambda_proxy.apigateway.Request
    """
    try:
        return get_response(event)

    except errors.BaseErrorX as e:
        Logger.exception(e.to_dict(), exc_info=e)
        return response_handler.response_error(e)

    except BaseException as e:
        Logger.exception(errors.BaseErrorX(str(e), 500, e.__class__.__name__).to_dict(), exc_info=e)
        return response_handler.response_error(errors.BaseErrorX(str(e), 500, e.__class__.__name__))
