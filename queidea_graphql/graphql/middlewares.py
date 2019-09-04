from graphql import GraphQLError
from promise import Promise
from queidea_graphql.graphql.errors import GenericError
from queidea_graphql.security.crypto import get_jwt_payload, resolve_identity

EMPTY_CONTEXT = {}
AUTH_USER = 'user_info'
DEFAULT_SECRET = 'secret'
DEFAULT_AUTH_HEADER = 'Authorization'
DEFAULT_AUTH_HEADER_PREFIX = 'JWT'
DEFAULT_ALGORITHM = 'HS256'
DEFAULT_CHECK_FN = None
DEFAULT_GET_PAYLOAD_FN = None
DEFAULT_ENABLED = True

WHITE_LIST = ['IntrospectionQuery']


class AuthenticationMiddleware(object):
    def __init__(self,
                 auth_header_prefix=DEFAULT_AUTH_HEADER_PREFIX,
                 resolve_identity=DEFAULT_CHECK_FN,
                 get_jwt_payload_fn=DEFAULT_GET_PAYLOAD_FN,
                 enabled=DEFAULT_ENABLED):
        self.resolve_identity = resolve_identity
        self.get_jwt_payload_fn = get_jwt_payload_fn
        self.auth_header_prefix = auth_header_prefix
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
            return Promise.reject(GraphQLError(e.message))

        # if auth was present and it auth checking was successful then
        # keep going to the next fetcher
        return next(root, info, **kwargs)

    def check_auth(self, authorization_value):
        """
        Checks whether the token is valid and it carries a valid identity
        """

        payload = self.get_jwt_payload_fn(authorization_value=authorization_value,
                                          auth_header_prefix=self.auth_header_prefix, secret=self.secret,
                                          algorithm=self.algorithm)

        if not payload:
            raise GenericError('API_ERRORS.INVALID_TOKEN')

        identity = self.resolve_identity(payload)

        if identity is None:
            raise GenericError('API_ERRORS.INVALID_JWT')

        return {AUTH_USER: identity}


auth_middleware = AuthenticationMiddleware(resolve_identity=resolve_identity,
                                           get_jwt_payload_fn=get_jwt_payload)
