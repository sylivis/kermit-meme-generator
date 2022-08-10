from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'User {self.email} has been added to the database'


class Empty_Template(db.Model):
    id = db.Column(db.String, primary_key=True)
    filename = db.Column(db.String(200))
    user_added = db.Column(db.String, db.ForeignKey('user.token'))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   
    def __init__(self, filename, user_token, id=''):
        self.id = self.set_id()
        self.filename = filename
        self.user_added = user_token

    def set_id(self):
        return (secrets.token_urlsafe())

    def __repr__(self) -> str:
        return f'succesfully added template'


class Meme(db.Model):
    id = db.Column(db.String, primary_key=True)
    image_id = db.Column(db.String(300))
    caption = db.Column(db.String(200))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
        
    def __init__(self, image_id, caption, user_token, id=''):
        self.id = self.set_id()
        self.image_id = image_id
        self.caption = caption
        self.user_token = user_token

    def __repr__(self):
        return 'succsefully created meme'
    
    def set_id(self):
        return (secrets.token_urlsafe())

class templateSchema(ma.Schema):
    class Meta:
        fields = ['id', 'filename', 'user_added']

da_template = templateSchema()
da_templates = templateSchema(many=True)


class meme_Schema(ma.Schema):
    class Meta:
        fields = ['id', 'image_id', 'caption']

da_meme = meme_Schema()
da_memes = meme_Schema(many=True)