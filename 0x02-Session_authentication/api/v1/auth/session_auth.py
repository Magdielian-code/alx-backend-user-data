#!/usr/bin/env python3
"""
class to manage the API authentication.
"""


from api.v1.auth.auth import Auth
from models.user import User
import uuid
from models.user import User


class SessionAuth(Auth):
    """SessionAuth class to manage the API authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID for a user ID"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with a given session ID.

        Args:
            session_id (str): The session ID to retrieve the user
                ID for.

        Returns:
            str: The user ID associated with the session ID, or None
                if the session ID is invalid.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves the currently authenticated user.

        Args:
            request (Request): The request object (optional).

        Returns:
            User: The currently authenticated user.

        """
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """
        Destroys a session.

        Args:
            request (Request): The request object.

        Returns:
            bool: True if the session is successfully
                destroyed, False otherwise.
        """
        if request is None:
            return False
        cookie = self.session_cookie(request)
        if cookie is None:
            return False
        user_id = self.user_id_for_session_id(cookie)
        if user_id is None:
            return False
        del SessionAuth.user_id_by_session_id[cookie]
        return True