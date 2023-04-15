from core.models import DatabaseInfo


def database_exists(user_id: int) -> DatabaseInfo | None:
    return DatabaseInfo.objects.filter(user__id=user_id).first()
