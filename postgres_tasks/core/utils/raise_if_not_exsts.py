from rest_framework.exceptions import NotFound


def raise_if_not_exists(obj, message: str):
    if not obj:
        raise NotFound(detail=message)
