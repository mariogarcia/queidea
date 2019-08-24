from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from queidea_graphql.db.db import Base


class Link(Base):
    __tablename__ = 'links'
    uuid = Column(UUID(as_uuid=True), primary_key=True)
    description = Column(String)
    uri = Column(String)
