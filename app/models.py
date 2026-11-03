from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id, name, email, is_active):
        self.id = user_id
        self.name = name
        self.email = email
        self.active = is_active

    @property
    def is_active(self):
        return self.active