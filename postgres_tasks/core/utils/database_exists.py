from core.models import DatabaseInfo


def database_exists(user_id: int) -> bool:
    return DatabaseInfo.objects.filter(user__id=user_id).exists()
