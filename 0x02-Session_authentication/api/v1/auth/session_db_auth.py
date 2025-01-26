
#!/usr/bin/env python3
"""
class to manage the API authentication.
"""


from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionExpAuth class to manage the API authentication"""

    def create_session(self, user_id=None):
        if user_id is None:
            return None
        sess = UserSession(user_id=user_id, created_at=datetime.now())
        sess.save()
        return sess.id

    def user_id_for_session_id(self, session_id=None):
        if session_id is None:
            return None
        data = UserSession.serach({'session_id': session_id})
        if data:
            return data[0].user_id

        return None

    def destroy_session(self, request=None):
        sess_id = self.session_cookie(request)
        if sess_id:
            user_sess = UserSession.search({'session_id': sess_id})
            for user_s in user_sess:
                user_s.remove()
