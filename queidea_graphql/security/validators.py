from authlib.oauth2.rfc6750 import BearerTokenValidator
from .models import Token


class TokenValidator(BearerTokenValidator):
    def request_invalid(self, request):
        return False

    def token_revoked(self, token):
        return False

    def authenticate_token(self, token_string):
        print('==============>{}'.format(token_string))
        return Token()
