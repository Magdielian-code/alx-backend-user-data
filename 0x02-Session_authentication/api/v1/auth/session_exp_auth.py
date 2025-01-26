
#!/usr/bin/env python3
"""
class to manage the API authentication.
"""


from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class to manage the API authentication"""
    user_id_by_session_id = {}

    def __init__(self):
        """
        Initializes a new instance of the SessionExpAuth class.
        The session_duration is set based on the value of the
        SESSION_DURATION environment variable.
        """
        self.session_duration = int(os.getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """
        Create a new session for the specified user.

        Args:
          user_id (str): The ID of the user for whom the session
          is being created.

        Returns:
          str: The session ID if the session was created
          successfully, None otherwise.
        """
        sess_id = super().create_session(user_id)
        if sess_id is None:
            return None
        SessionExpAuth.user_id_by_session_id[sess_id] = \
            {'user_id': user_id, 'created_at': datetime.now()}
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with a given session ID.

        Args:
          session_id (str): The session ID to retrieve the user
          ID for.

        Returns:
          int or None: The user ID associated with the session
          ID, or None if the session ID is invalid or expired.
        """
        if session_id is None:
            return None
        if session_id not in SessionExpAuth.user_id_by_session_id:
            return None
        user_data = SessionExpAuth.user_id_by_session_id.get(
            session_id
        )
        if self.session_duration <= 0:
            return user_data.get('user_id')
        if 'created_at' not in user_data:
            return None

        created_at = user_data['created_at']
        session_duration = self.session_duration

        exp_time = created_at + timedelta(seconds=session_duration)

        current_datetime = datetime.now()
        if exp_time < current_datetime:
            return None

        return user_data.get('user_id')
