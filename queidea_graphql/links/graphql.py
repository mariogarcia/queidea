from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import Link as LinkModel


class Link(SQLAlchemyObjectType):
    class Meta:
        model = LinkModel
        interfaces = (relay.Node, )


class LinkConnection(relay.Connection):
    class Meta:
        node = Link
