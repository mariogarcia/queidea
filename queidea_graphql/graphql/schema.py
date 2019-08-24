from graphene import ObjectType, Schema
from graphene_sqlalchemy import SQLAlchemyConnectionField


from queidea_graphql.links import graphql as graphql_links


class Query(ObjectType):
    all_links = SQLAlchemyConnectionField(graphql_links.LinkConnection)


schema = Schema(query=Query)
