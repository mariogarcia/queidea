from queidea_graphql.config.logger import log
from queidea_graphql.config.db import db_session
from .models import Link


def save(group_id, description, uri):
    """
    Saves a new link
    """
    log.msg("link/create", group_id=group_id, uri=uri)
    link_to_save = Link(group_id=group_id, description=description, uri=uri)

    db_session.add(link_to_save)
    db_session.commit()

    return link_to_save
