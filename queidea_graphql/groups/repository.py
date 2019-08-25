from queidea_graphql.config.logger import log
from queidea_graphql.config.db import db_session
from queidea_graphql.config.uuid import generate_id
from .models import Group


def save(name):
    """
    Saves a new group with the name passed
    as argument
    """
    log.msg("group/create", name=name)
    group_uuid = generate_id()
    group_to_save = Group(
        uuid=group_uuid,
        name=name
    )

    try:
        db_session.add(group_to_save)
        db_session.commit()
        log.msg("group/create/success", uuid=group_uuid)
    except:
        log.msg("group/create/failure")
        db_session.rollback()

    return group_to_save
