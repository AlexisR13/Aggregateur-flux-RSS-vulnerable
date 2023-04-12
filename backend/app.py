from flask import Flask, request, jsonify, redirect, url_for, flash
from flask_login import login_user, UserMixin, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import feedparser
import bcrypt
from hmac import compare_digest
import ssl
import re

#Fonctionnalités bonus si on à le temps:

# rendre l'authentification galère avec vérification d'email et captcha.
# mieux gérer l'unicité du username
# éviter les timings attacks
# recommendation de flux à partir de ceux stockés dans la DB
    # en utilisant la similarité des flux favoris, ou encore juste la liste des flux associés au compte


# Il faut créer une table d'association pour les favoris, les articles sauvegardés et aussi les articles abonnés

    

"""
parent = Parent(name='John')
child1 = Child(name='Alice')
child2 = Child(name='Bob')
parent.children = [child1, child2]
db.session.add(parent)
db.session.commit()

parent = Parent.query.get(1)
children = parent.children
"""

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'a random string which I found on some w3ird internet website'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'  #local database for now
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


# Avoid error checking TLS certificate
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


#Stocker les feeds favoris des personnes dans la DB User, ou juste leur lien ?
#ou créer un table dse feeds sauvegardés avec un array des users ID

#PAS SUR DES BACKREFS

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
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

    """ def __init__(self,name, url, bool=False):
        
        self.name=name
        self.url=url
        self.defaults = bool """
    
#many-to-many mapping
filter_feeds = db.Table('filter_feeds',
    db.Column('filter_id', db.Integer, db.ForeignKey('filter.id')),
    db.Column('feed_id', db.Integer, db.ForeignKey('feed.id'))
    )

    
class Filter(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.Text) 
    rule = db.Column(db.Text)  
    feeds = db.relationship('Feed', secondary=filter_feeds, backref='feeds')
    
    """def __init__(self,name, owner_id, rule=""):
        
        self.name=name
        self.rule=""
        self.owner_id = owner_id"""




FEEDS = {
    # 'feed_name' : 'feed_url',
    'ANSSI_publications': 'http://www.ssi.gouv.fr/feed/publication/',
    'ANSSI_actualites': 'https://www.ssi.gouv.fr/feed/actualite/',
    'CERTFR_alertes': 'https://www.cert.ssi.gouv.fr/alerte/feed/',
    'CERTFR_menaces_et_incidents': 'https://www.cert.ssi.gouv.fr/cti/feed/',
    'CERTFR_avis': 'https://www.cert.ssi.gouv.fr/avis/feed/'
}

#Il faudrait avoir une vue un peu comme dans gmail, avec une liste limitée de flux.
#Avec un bouton  "en savoir plus", ça serait top si on peut afficher directement dans le navigateur le contenu de la page web

@app.route('/')
def show_feeds():
    dic = {}
    
    if current_user.is_authenticated:
        user_id = current_user.get_id()
        feeds = Feed.query.filter_by(owner_id = int(user_id)).all()
    else:
        feeds = Feed.query.filter_by(default=True).all()
        
    for feed in feeds:
        dic[feed.name] = feed.url
        
    return jsonify(dic)
    

@app.route('/signup', methods=["POST"])
def signup():
    
    username = request.json.get('login')  #or login ..
    password = request.json.get('password')   #should have password confirmation
    email = request.json.get('email')

    #https://stackoverflow.com/questions/25211924/check-every-condition-in-python-if-else-even-if-one-evaluates-to-true
    errors = [message for (has_error, message) in (
        (len(password)<12, 'Password must be at least 12 characters long.'),
        (re.search(r'[A-Z]', password) is None, 'Password must include upper case letters.'),
        (re.search(r'[a-z]', password) is None, 'Password must include lower case letters.'),
        (re.search(r'\d', password) is None, 'Password must include digits.'),
        (re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is None, 'Invalid email.'),
        (User.query.filter_by(login=username).first(), 'Username already taken')
        ) if has_error]
    
    if len(errors)>0:
        return jsonify({'success': False, "message":"\n".join(errors)})

    user = User(username,password, email)
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=True)
    
    return jsonify({'success': True})


@app.route('/login', methods=["POST"])
def login():
    username = request.json.get('login')
    password = request.json.get('password').encode()
    user = User.query.filter_by(login=username).first()
    #login with email ?
    
    if user and compare_digest(bcrypt.hashpw(password, user.password), user.password):  #failed connexion
        login_user(user, remember=True)
        return jsonify({'success': True})
        
    return jsonify({'success': False, "message":"Identifiant ou mot de passe incorrect."})



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'success': True})

@app.route('/profile')
@login_required
def profile():
    # Afficher un menu pour le profil avec plusieurs sous-options:
        # modification de mdp
        # modification d'email
        # suppression du compte/effaçage des données
        # ajout d'un flux RSS
    return redirect(url_for('index'))


@app.route('/<feed_name>')
def get_feed(feed_name):
    if feed_name not in FEEDS.keys():
       return 'Feed not found'
    feed_url = FEEDS[feed_name]
    feed = feedparser.parse(feed_url)
    return feed['entries']

@app.route('/<feed_name>/<article_id>')
def get_article(feed_name, article_id):
    if feed_name not in FEEDS.keys():
       return 'Feed not found'
    feed_url = FEEDS[feed_name]
    feed = feedparser.parse(feed_url)
    articles = feed['entries']
    if int(article_id) >= len(articles):
       return 'Article not found'
    return articles[int(article_id)]


if __name__ == "__main__":
    
    with app.app_context():
        
        db.drop_all() #FOR TESTING PURPOSES ONLY
        
        db.create_all()
        
        default_feeds = []
        
        for key in FEEDS:
            default_feeds.append(Feed(name=key, url=FEEDS[key], default=True))
            
        db.session.add_all(default_feeds)
        
        admin = User("admin","aV3rySecurePassworth(haha)!", "moietmoimoimoi@gmail.com")
        db.session.add(admin)
        
        db.session.commit()
        

    
    app.run(port=5000, debug=True)