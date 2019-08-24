from queidea_graphql.config.logger import log
from queidea_graphql.config.db import db_session
from .models import Group


def save(name):
    """
    Saves a new group with the name passed
    as argument
    """
    log.msg("group/create", name=name)
    group_to_save = Group(name=name)

    db_session.add(group_to_save)
    db_session.commit()

    return group_to_save
