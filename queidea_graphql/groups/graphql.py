from graphene import relay, Mutation, Field, String, Boolean
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import Group as GroupModel
from .repository import save


class Group(SQLAlchemyObjectType):
    class Meta:
        model = GroupModel
        interfaces = (relay.Node,)


class GroupConnection(relay.Connection):
    class Meta:
        node = Group


class CreateGroup(Mutation):
    """
    Mutation to create a new group
    """
    class Arguments:
        name = String(required=True)

    ok = Boolean()
    group = Field(lambda: Group)

    def mutate(root, info, name):
        saved_group = save(name)
        return CreateGroup(ok=True, group=saved_group)
