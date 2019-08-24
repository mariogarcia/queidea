from flask import Flask
from flask_graphql import GraphQLView
from queidea_graphql.graphql import schema


app = Flask(__name__)


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
