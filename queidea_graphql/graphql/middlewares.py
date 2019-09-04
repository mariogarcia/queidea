from graphql import GraphQLError
from promise import Promise
from queidea_graphql.config.logger import log
from queidea_graphql.graphql.errors import GenericError
from queidea_graphql.security.crypto import get_jwt_payload, resolve_identity
from queidea_graphql.config.yaml import config

EMPTY_CONTEXT = {}
AUTH_USER = 'user_info'
WHITE_LIST = ['IntrospectionQuery']


class AuthenticationMiddleware(object):
    def __init__(self,
                 auth_header_prefix,
                 resolve_identity,
                 get_jwt_payload_fn,
                 secret,
                 algoritm,
                 enabled):
        self.resolve_identity = resolve_identity
        self.get_jwt_payload_fn = get_jwt_payload_fn
        self.auth_header_prefix = auth_header_prefix
        self.secret = secret
        self.algorithm = algoritm
        self.enabled = enabled

    def resolve(self, next, root, info, **kwargs):
        """
        Will check whether authentication is required or not
        """
        # if security is disabled bypass auth (enabled by default)
        if not self.enabled:
            return next(root, info, **kwargs)

        # if no context is present then require auth
        if not info.context:
            return Promise.reject(GraphQLError('API_ERRORS.BAD_CREDENTIALS'))

        # Convert the context into a dictionary
        info.context = {'request': info.context}

        # if white-listed bypass auth
        white_listed = info.operation.name and info.operation.name.value in WHITE_LIST
        if white_listed:
            return next(root, info, **kwargs)

        local_request = info.context.get('request')
        auth_present = DEFAULT_AUTH_HEADER in local_request.headers

        # if no auth header is present then require auth
        if not auth_present:
            return Promise.reject(GraphQLError('API_ERRORS.BAD_CREDENTIALS'))

        # adds identity to execution context
        try:
            user_info = self.check_auth(local_request.headers[DEFAULT_AUTH_HEADER])
            info.context = info.context.copy()
            info.context.update(user_info)
        except GenericError as e:
            log.error("middleware/auth/error", headers=local_request.headers)
            return Promise.reject(GraphQLError(e.message))

        # if auth was present and it auth checking was successful then
        # keep going to the next fetcher
        return next(root, info, **kwargs)

    def check_auth(self, authorization_value):
        """
        Checks whether the token is valid and it carries a valid identity
        """
        payload = self.get_jwt_payload_fn(authorization_value=authorization_value,
                                          auth_header_prefix=self.auth_header_prefix,
                                          secret=self.secret,
                                          algorithm=self.algorithm)

        if not payload:
            raise GenericError('API_ERRORS.INVALID_TOKEN')

        identity = self.resolve_identity(payload)

        if identity is None:
            raise GenericError('API_ERRORS.INVALID_JWT')

        return {AUTH_USER: identity}


DEFAULT_SECRET = config.security.secret or 'secret'
DEFAULT_AUTH_HEADER = config.security.header or 'Authorization'
DEFAULT_AUTH_HEADER_PREFIX = config.security.prefix or 'JWT'
DEFAULT_ALGORITHM = config.security.algorithm or 'HS256'
DEFAULT_RESOLVE_IDENTITY = resolve_identity
DEFAULT_GET_PAYLOAD_FN = get_jwt_payload
DEFAULT_ENABLED = True

auth_middleware = AuthenticationMiddleware(
    auth_header_prefix=DEFAULT_AUTH_HEADER_PREFIX,
    resolve_identity=DEFAULT_RESOLVE_IDENTITY,
    get_jwt_payload_fn=DEFAULT_GET_PAYLOAD_FN,
    secret=DEFAULT_SECRET,
    algoritm=DEFAULT_ALGORITHM,
    enabled=DEFAULT_ENABLED
)
