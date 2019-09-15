import yaml
import os
from .logger import log


# For development puposes we look for the current directory
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))


# Wraps security configuration properties
class Security(object):
    def __init__(self, secret=None, algorithm=None, header=None, prefix=None, audience=None):
        self.secret = secret
        self.algorithm = algorithm
        self.header = header
        self.prefix = prefix
        self.audience = audience


# Wraps database configuration properties
class Database(object):
    def __init__(self, url=None):
        self.url = url


# Wraps configuration properties
class Configuration(object):
    def __init__(self, database, security, cors):
        self.database = Database(**database)
        self.security = Security(**security)
        self.cors = Cors(**cors)


# Cors configuration
class Cors(object):
    def __init__(self, enabled):
        self.enabled = enabled


# Creates application's configuration from a given
# file taken or from the path described in the env
# variables `QUEIDEA_CONFIG_PATH` or from a config
# file `config.yaml` located in the `CONFIG_DIR`
# path
def create_config(config_file_path):
    """
    Loads configuration from a yaml file located or where the
    environment variable `QUEIDEA_CONFIG_PATH` says or
    `config.yaml` file in this directory
    """
    with open(config_file_path) as stream:
        try:
            configuration = yaml.safe_load(stream)
            return Configuration(
                configuration['database'],
                configuration['security'],
                configuration['cors']
            )
        except yaml.YAMLError as error:
            log.error(error)


# default path to get the config file
environ_path = os.environ.get('QUE_IDEA_CONFIG_PATH')

# second option to get the config file
fallback_path = os.path.join(CONFIG_DIR, 'config.yaml')

# configuration instance created from confi path
config = create_config(environ_path or fallback_path)
