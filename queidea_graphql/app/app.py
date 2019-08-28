from flask import Flask
from flask_graphql import GraphQLView
from queidea_graphql.graphql import schema
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


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
