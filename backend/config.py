from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import ssl

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from datetime import timedelta


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
#a supprimer ?

# SQL Database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'  #local database for now
db = SQLAlchemy(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret, thou2 shall() not find/ it. " 
ACCESS_EXPIRES = timedelta(hours=2)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)


"""login_manager = LoginManager()
login_manager.init_app(app)"""


FEEDS = {
    # 'feed_name' : 'feed_url',
    'ANSSI publications': 'http://www.ssi.gouv.fr/feed/publication/',
    'ANSSI actualites': 'https://www.ssi.gouv.fr/feed/actualite/',
    'CERTFR alertes': 'https://www.cert.ssi.gouv.fr/alerte/feed/',
    'CERTFR menaces & incidents': 'https://www.cert.ssi.gouv.fr/cti/feed/',
    'CERTFR avis': 'https://www.cert.ssi.gouv.fr/avis/feed/'
}

# Avoid error checking TLS certificate
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context