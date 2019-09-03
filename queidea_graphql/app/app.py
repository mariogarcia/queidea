from flask import Flask
from flask_graphql import GraphQLView

from authlib.flask.oauth2 import ResourceProtector
from queidea_graphql.graphql import schema
from queidea_graphql.security.validators import TokenValidator


app = Flask(__name__)


require_oauth = ResourceProtector()
require_oauth.register_token_validator(TokenValidator())


# Receives user authentication token and passes it
# to the GraphQL context
def auth_required(fn):
    def wrapper(*args, **kwargs):
        with require_oauth.acquire('utilitys') as token:
            print('==============>{}'.format(token))
        return fn(*args, **kwargs)
    return wrapper


# Processes GraphQL requests
def graphql_view():
    view = GraphQLView.as_view(
        'graphql',
        schema=schema.schema,
        graphiql=False
    )
    return auth_required(view)


# Starts up application
def runapp():
    app.add_url_rule(
        "/graphql",
        view_func=graphql_view()
    )
    app.run()
