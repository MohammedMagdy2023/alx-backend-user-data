#!/usr/bin/env python3
"""
Basic auth module for the API
"""
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """
    The template for basic authentication module
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract the Base64 encoded characters
        """
        if authorization_header is None:
            return None
        if isinstance(authorization_header, str):
            if authorization_header[0:6] != "Basic ":
                return None
            return authorization_header[6:]
        else:
            return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """ Decode Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            auth = base64_authorization_header.encode('utf-8')
            auth = base64.b64decode(auth)
            return auth.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ extract_user_credentials
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        email, password = decoded_base64_authorization_header.split(":")
        return (email, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ returns the User instance based on his email and password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None
