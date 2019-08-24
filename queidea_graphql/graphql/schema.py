from graphene import ObjectType, String, Schema, Field

from queidea_graphql.links import links

class Query(ObjectType):
    link = Field(links.Link)

schema = Schema(query=Query)