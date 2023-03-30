from typing import TypedDict

from core.models import DatabaseInfo


class WebErrorData(TypedDict):
    data: dict
    status: int


def check_db_creation_ability(user_id: int) -> WebErrorData | None:
    if DatabaseInfo.objects.filter(user__id=user_id).exists():
        return WebErrorData(data={'detail': 'Active database already exists'}, 
                            status=400)
    return None
