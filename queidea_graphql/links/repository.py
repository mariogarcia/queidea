from queidea_graphql.config.logger import log
from queidea_graphql.config.db import db_session
from queidea_graphql.config.uuid import generate_id
from .models import Link


def save(group_id, description, uri):
    """
    Saves a new link
    """
    log.msg("link/create", group_id=group_id, uri=uri)
    link_uuid = generate_id()
    link_to_save = Link(
        uuid=link_uuid,
        group_id=group_id,
        description=description, uri=uri
    )

    try:
        db_session.add(link_to_save)
        db_session.commit()
        log.msg("link/create/success", uuid=link_uuid)
    except:
        log.msg("link/create/failure")
        db_session.rollback()

    return link_to_save
