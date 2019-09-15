from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from queidea_graphql.config import yaml
from queidea_graphql.config.logger import log
from queidea_graphql.graphql import schema
from queidea_graphql.graphql.middlewares import auth_middleware


# create new Flask app
app = Flask(__name__)


# enable cors if necessary
if yaml.config.cors.enabled:
    log.debug('app/cors', cors=yaml.config.cors.enabled)
    CORS(app)


# startup app
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
