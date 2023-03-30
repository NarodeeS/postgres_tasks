from .errors.bad_request_error import BadRequestError


def raise_if_exists(obj, message: str):
    if obj:
        raise BadRequestError(message)
