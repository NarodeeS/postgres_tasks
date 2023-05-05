from core.models import DatabaseInfo
from core.tasks import delete_db_task
from .errors import NoSuchDbError


def delete_db(db_name: str):
    database_info = (DatabaseInfo.objects
                                 .filter(db_name=db_name)
                                 .first())
    if not database_info:
        raise NoSuchDbError(db_name)
    delete_db_task.delay(db_name)
