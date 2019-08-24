from flask import Flask
from flask_graphql import GraphQLView

app = Flask(__name__)

# from queidea_graphql.graphql.schema import schema
from queidea_graphql.graphql import schema


def runapp(): 
    app.add_url_rule(
        "/graphql", 
        view_func=GraphQLView.as_view(
            "graphql", 
            schema=schema.schema, 
            grapiql=False
        )
    )
    app.run() 
