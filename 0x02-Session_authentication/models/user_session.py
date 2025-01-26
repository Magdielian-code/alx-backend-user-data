
#!/usr/bin/env python3
"""
User Session module
"""
from models.base import Base


class UserSession(Base):
    """
    User Session class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User Session instance
        """

        self.user_id = kwargs.get('user_id', None)
        self.session_id = kwargs.get('session_id', None)
        super().__init__(*args, **kwargs)
