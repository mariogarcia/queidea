from flask import Flask
from flask_graphql import GraphQLView
from queidea_graphql.graphql import schema
from queidea_graphql.graphql.middlewares import auth_middleware


app = Flask(__name__)


def runapp():
    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema.schema,
            graphiql=False,
            middleware=[auth_middleware]
        )
    )
    app.run()
