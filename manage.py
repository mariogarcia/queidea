import click
from queidea_graphql import app
from queidea_fixtures import fixtures


@click.group()
def cli():
    pass


@cli.command()
def runserver():
    """
    Starts up queidea GraphQL api (development)
    """
    app.runapp()


@cli.command()
def create_schema():
    """
    Creates model schema in the database
    """
    fixtures.create_schema()


@cli.command()
def add_fixtures():
    """
    Adds fixtures data to app
    """
    fixtures.create_data()


if __name__ == '__main__':
    cli()
