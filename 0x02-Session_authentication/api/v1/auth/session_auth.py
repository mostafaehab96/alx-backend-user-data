#!/usr/bin/env python3
"""
Session class module
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    Session class that handles session authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session id for the user with user_id"""
        if type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns user id based on session id."""
        if type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """Returns current user from the cookie value"""
        session_id = self.session_cookie(request)
        if session_id:
            user_id = self.user_id_for_session_id(session_id)
            return User.get(user_id)

    def destroy_session(self, request=None):
        """Deletes the user session / logout"""

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
