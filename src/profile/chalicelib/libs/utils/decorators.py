import json
import os
from datetime import date, datetime
from typing import Any, Dict, Union

from chalice import Blueprint, Chalice
from chalice.app import Request
from jsonschema import exceptions, validate
from ... import logger
from . import errors


class Options(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)

    def get(self, key, default=None):
        value = getattr(self, key)
        return value if value is not None else default

    def __getattr__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            return None

    def to_dict(self) -> Dict[Any, Any]:
        # Don't copy internal attributes.
        copied = {
            k: v for k, v in self.__dict__.items()
            if not k.startswith('_')
        }

        return copied


def _dict_to_options(d):
    dict_ = json.loads(json.dumps(d, default=json_default))
    return Options(dict_)


def json_default(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    else:
        return str(obj)


def get_formatted_error_messages(validation_error: exceptions.ValidationError):
    debug_message: str = f"Validation Error: path {validation_error.json_path}, problem: {validation_error.message}"
    pretty_message: str = validation_error.schema.get("messages", {}).get(validation_error.validator)

    if not pretty_message:
        if os.environ["ENV"] == "prod":
            field_name = str(validation_error.json_path).lstrip("$.").split(".")[-1]
            pretty_message = f"Validation error of {field_name}" if field_name else "Validation error"
        else:
            pretty_message = debug_message

    return debug_message, pretty_message


def validate_request_data(blueprint: Union[Chalice, Blueprint], schema: dict, convert_options_to_object=True):
    def decorator(func):
        def validate_func(**kwargs):
            blueprint.current_request.options = get_validated_data(
                data=blueprint.current_request.options,
                schema=schema,
                convert_data_to_object=convert_options_to_object)

            return func(**kwargs)
        return validate_func
    return decorator


def validate_event_data(event: Request, schema: dict, convert_options_to_object=True):
    def decorator(func):
        def validate_func(**kwargs):
            event.options = get_validated_data(
                data=event.options,
                schema=schema,
                convert_data_to_object=convert_options_to_object)

            return func(**kwargs)
        return validate_func
    return decorator


def get_validated_data(data: dict, schema: dict, convert_data_to_object=False) -> Union[dict, Options]:
    try:
        logger.Logger.debug("Trying to validate data using schema: %s", schema)
        validate(instance=data, schema=schema)

        if convert_data_to_object:
            data = _dict_to_options(data)

        return data

    except exceptions.ValidationError as validation_error:
        error_messages = get_formatted_error_messages(validation_error)
        raise errors.ValidationErrorX(error_messages, validation_error.json_path)
    except exceptions.SchemaError as schema_error:
        raise errors.ValidationErrorX(schema_error.message, schema_error.json_path)


def validate_data(data: dict, schema: dict, convert_data_to_object=False):
    def decorator(func):
        def validate_func(**kwargs):
            get_validated_data(data, schema, convert_data_to_object)
            return func(**kwargs)
        return validate_func
    return decorator
