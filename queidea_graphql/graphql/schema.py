from graphene import ObjectType, Schema
from graphene_sqlalchemy import SQLAlchemyConnectionField


from queidea_graphql.links import graphql as graphql_links
from queidea_graphql.groups import graphql as graphql_groups


class Query(ObjectType):
    """
    Represents all queries
    """
    all_links = SQLAlchemyConnectionField(graphql_links.LinkConnection)
    all_groups = SQLAlchemyConnectionField(graphql_groups.GroupConnection)


class Mutation(ObjectType):
    """
    Represents all operations to create/modify/delete instances
    """
    create_group = graphql_groups.CreateGroup.Field()


schema = Schema(query=Query, mutation=Mutation)
