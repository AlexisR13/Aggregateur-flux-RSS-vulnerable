
from config import *


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    login = db.Column(db.String(100), unique=True)  #login has to be unique
    password = db.Column(db.LargeBinary)  #hash of password
    email = db.Column(db.Text)
    
    feeds = db.relationship('Feed', backref='user')
    filters = db.relationship('Filter', backref='user')

    def __init__(self,login,passwd, email=""):
        
        self.login=login
        self.password=bcrypt.hashpw(passwd.encode(), bcrypt.gensalt())
        self.email = email
    
    
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Feed(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.Text, nullable=False, unique=True)  #url for feed, maybe not enough length
    name = db.Column(db.Text)  #name might not be unique
    default = db.Column(db.Boolean, nullable=False)  #url for feed, maybe not enough length
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
#many-to-many mapping
filter_feed = db.Table('filter_feed',
    db.Column('filter_id', db.Integer, db.ForeignKey('filter.id')),
    db.Column('feed_id', db.Integer, db.ForeignKey('feed.id'))
    )

    
class Filter(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.Text) 
    rule = db.Column(db.Text)  
    feeds = db.relationship('Feed', secondary=filter_feed, backref='filters')
