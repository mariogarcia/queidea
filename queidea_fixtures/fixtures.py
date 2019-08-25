from queidea_graphql.config.db import Base, engine, db_session
from queidea_graphql.config.uuid import generate_id
from queidea_graphql.groups.models import Group
from queidea_graphql.links.models import Link
from queidea_graphql.config.logger import log


def create_schema():
    """
    Creates database schema
    """
    log.msg("fixtures/schema")
    Base.metadata.create_all(bind=engine)
    log.msg("fixtures/schema/success")


def create_data():

    """
    Adds data to database
    """
    group = Group(uuid=generate_id(), name="programming")
    db_session.add(group)
    log.msg("fixtures/data/group", uuid=group.uuid, name=group.name)

    for i in range(1, 10):
        link = Link(
            uuid=generate_id(),
            uri="https://www.google.es",
            description="description",
            group_id=group.uuid)

        db_session.add(link)
        log.msg("fixtures/data/link", uuid=link.uuid, uri=link.uri, group=group.uuid)

    try:
        db_session.commit()
        log.msg("fixtures/data/success")
    except Exception as err:
        db_session.rollback()
        log.msg("fixtures/data/error", err=err)
