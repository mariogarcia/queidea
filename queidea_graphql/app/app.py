from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from queidea_graphql.graphql import schema
from queidea_graphql.graphql.middlewares import auth_middleware


app = Flask(__name__)
CORS(app)


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
