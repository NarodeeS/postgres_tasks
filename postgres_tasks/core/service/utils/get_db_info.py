from core.models import DatabaseInfo
from ..errors.no_such_db_error import NoSuchDbError


def get_db_info(db_name: str) -> DatabaseInfo:
    potential_db_info = (DatabaseInfo.objects
                                     .filter(db_name=db_name)
                                     .first())
    if not potential_db_info:
        raise NoSuchDbError(db_name)
    return potential_db_info
