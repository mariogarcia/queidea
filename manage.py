from queidea_graphql import app
from queidea_fixtures import fixtures


def runserver():
    """
    Starts up queidea GraphQL api (development)
    """
    app.runapp()


def create_schema():
    fixtures.create_schema()


def add_fixtures():
    """
    Adds fixtures data to app
    """
    fixtures.create_data()
