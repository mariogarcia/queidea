from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from queidea_graphql.config.db import Base


class Link(Base):
    __tablename__ = 'link'
    uuid = Column(UUID(as_uuid=True), primary_key=True)
    description = Column(String)
    uri = Column(String)

    group_id = Column(UUID, ForeignKey("group.uuid"), nullable=False)
