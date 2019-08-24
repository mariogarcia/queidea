from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from queidea_graphql.config.db import Base


class Group(Base):
    __tablename__ = 'group'
    uuid = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String)
