from graphene import relay, String, Boolean, Field, Mutation
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import Link as LinkModel
from .repository import save


class Link(SQLAlchemyObjectType):
    class Meta:
        model = LinkModel
        interfaces = (relay.Node, )


class LinkConnection(relay.Connection):
    class Meta:
        node = Link


class CreateLink(Mutation):
    """
    Mutation to create a new link
    """
    class Arguments:
        group_id = String(required=True)
        description = String()
        uri = String()

    ok = Boolean()
    link = Field(lambda: Link)

    def mutate(root, info, name):
        saved_group = save(name)
        return CreateLink(ok=True, group=saved_group)
