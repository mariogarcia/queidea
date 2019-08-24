from graphene import ObjectType, String


class Link(ObjectType):
    name = String(default_value="Link")
    description = String()
    url = String()
