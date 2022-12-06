from api import db, Config
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import URLSafeSerializer, BadSignature


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(32), nullable=False, server_default="simple")

    def __init__(self, username, password, role="simple"):
        self.username = username
        self.hash_password(password)
        self.role = role

    def get_roles(self):
        return self.role

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self):
        s = URLSafeSerializer(Config.SECRET_KEY)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = URLSafeSerializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except BadSignature:
            return None  # invalid token
        user = UserModel.query.get(data['id'])
        return user
