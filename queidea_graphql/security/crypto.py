from jwt import InvalidTokenError, decode
from queidea_graphql.graphql.errors import GenericError


def get_jwt_payload(authorization_value, auth_header_prefix=None, secret=None, algorithm=None):
    """
    Checks whether the token is valid and it carries a valid identity
    """
    try:
        items = authorization_value.split()

        if not len(items) == 2:
            return None

        prefix = items[0]
        token = items[1]

        # checking prefix
        if prefix != auth_header_prefix:
            return None

        payload = decode(token, secret, algorithms=[algorithm])
    except InvalidTokenError:
        return None

    return payload


def resolve_identity(payload, allow_device_tokens=False, leeway_minutes=0):
    """
    Resolves user basic security information such as email and roles
    """
    if not payload or 'email' not in payload or 'token' not in payload:
        raise GenericError('API_ERRORS.INVALID_JWT_PAYLOAD')

    email = payload['email']
    roles = payload['roles']

    if not email or roles:
        raise GenericError('API_ERRORS.BAD_CREDENTIALS')

    return payload


def get_authorized_user_via_token(authorization_value, allow_device_tokens=False, leeway_minutes=0):
    """
    Gets user information from jwt payload (is it necessary?)
    """
    payload = get_jwt_payload(authorization_value=authorization_value)
    identity = None

    try:
        identity = resolve_identity(payload, allow_device_tokens, leeway_minutes)
    except GenericError:
        return None

    return identity
