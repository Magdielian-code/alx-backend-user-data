#!/usr/bin/env python3
"""
class to manage the API authentication.
"""


from api.v1.auth.auth import Auth
from typing import TypeVar
import base64
from models.user import User
import os


class BasicAuth(Auth):
    """BasicAuth class to manage the API authentication"""

    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """
        Extract the Base64 encoded part of a
        Basic Authorization header.

        Args:
          authorization_header (str): The authorization
              header from which the Base64 encoded string
              is to be extracted.

        Returns:
          str: The Base64 encoded string if the header is
              valid and contains the
              expected prefix. Otherwise, None.

        Note:
            This function only validates the prefix and
            the presence of the header. It does not validate
            whether the Base64 string is properly encoded or
            decode the Base64 string.
        """
        if authorization_header is None or not isinstance(
            authorization_header,
            str
        ):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """
        Decode a Base64 encoded authorization header
        into a UTF-8 string.

        Args:
            base64_authorization_header (str):
              The Base64 encoded string to decode.

        Returns:
            str: The decoded UTF-8 string if successful,
              otherwise None.
        """
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header,
            str
        ):
            return None

        try:
            base64_bytes = base64.b64decode(
                base64_authorization_header
            )
            return base64_bytes.decode('utf-8')
        except (base64.binascii.Error, ValueError):
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Extract user email and password from a decoded
        Base64 authorization header.

        Args:
            decoded_base64_authorization_header (str):
              The decoded Base64 string from which to extract
              credentials.

        Returns:
            tuple: A tuple containing the user email and password
              if successful, otherwise (None, None).
        """
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str)):
            return None, None

        first_colon_index = decoded_base64_authorization_header.find(':')
        if first_colon_index == -1:
            return None, None

        user_email = decoded_base64_authorization_header[:first_colon_index]
        user_pwd = decoded_base64_authorization_header[first_colon_index + 1:]

        return user_email, user_pwd

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """
        Retrieve a User instance based on email and password.

        Args:
            user_email (str): The email of the user.
            user_pwd (str): The password of the user.

        Returns:
            User: The User instance if found and password is valid,
              otherwise None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        if not os.path.exists(".db_User.json"):
            return None
        users = User.search({'email': user_email})
        if not users:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the User instance for a request using
        Basic Authentication.

        Args:
            request (Request): The Flask request object.
              Defaults to None.

        Returns:
            User: The User object if authentication is successful,
              None otherwise.
        """
        if request is None:
            return None

        authorization_header = request.headers.get('Authorization')
        base64_auth_header = self.extract_base64_authorization_header(
            authorization_header
        )
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header
        )

        user_email, user_pwd = self.extract_user_credentials(
            decoded_auth_header
        )

        user_instance = self.user_object_from_credentials(
            user_email,
            user_pwd
        )

        return user_instance