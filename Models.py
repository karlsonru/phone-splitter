
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, password):
        self.id = 1
        self.password = password
        self.password_hash = generate_password_hash(self.password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

user = User('siisltd')