import bcrypt
from datetime import datetime

from config import *


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    login = db.Column(db.String(100), unique=True)  #login has to be unique
    password = db.Column(db.LargeBinary)  #hash of password
    email = db.Column(db.Text)
    
    feeds = db.relationship('Feed', backref='user')
    filters = db.relationship('Filter', backref='user')

    def __init__(self,login,password, email=""):
        
        self.login=login
        self.password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.email = email
        
    def __str__(self):
        return f"User(login='{self.login}', pw_hash='{self.password}', email='{self.email}', created_at='{self.created_at}')"
    
 
class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
    

# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None

    
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


class Feed(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.Text, nullable=False, unique=True)  #url for feed, maybe not enough length
    name = db.Column(db.Text)  #name might not be unique
    default = db.Column(db.Boolean, nullable=False)  #url for feed, maybe not enough length
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __str__(self):
        return f"Feed(name='{self.name}', url='{self.url}', default='{self.default}', owner_id='{self.owner_id}')"
    
    
#many-to-many mapping
filter_feed = db.Table('filter_feed',
    db.Column('filter_id', db.Integer, db.ForeignKey('filter.id')),
    db.Column('feed_id', db.Integer, db.ForeignKey('feed.id'))
    )

    
class Filter(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.Text, nullable=False) 
    rule = db.Column(db.Text)  
    feeds = db.relationship('Feed', secondary=filter_feed, backref='filters')

    def __str__(self):
        return f"Filter(name='{self.name}', rule='{self.rule}', owner_id='{self.owner_id}')"
    