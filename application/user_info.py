class UserInfo:
    def __init__(self):
        self._user_id = None
        self._name = None
        self._updated_at = None
        self._created_at = None

    def create_user(self, user_id, name, updated_at=None, created_at=None):
        self._user_id = user_id
        self._name = name
        self._updated_at = updated_at
        self._created_at = created_at

    def update_user(self, user_id, name, updated_at=None, created_at=None):
        self._user_id = user_id
        self._name = name
        self._updated_at = updated_at
        self._created_at = created_at
