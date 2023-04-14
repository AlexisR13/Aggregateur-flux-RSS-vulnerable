from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import ssl

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

# SQL Database
app.config['SECRET_KEY'] = 'a random string which I found on some w3ird internet website'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'  #local database for now
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


FEEDS = {
    # 'feed_name' : 'feed_url',
    'ANSSI_publications': 'http://www.ssi.gouv.fr/feed/publication/',
    'ANSSI_actualites': 'https://www.ssi.gouv.fr/feed/actualite/',
    'CERTFR_alertes': 'https://www.cert.ssi.gouv.fr/alerte/feed/',
    'CERTFR_menaces_et_incidents': 'https://www.cert.ssi.gouv.fr/cti/feed/',
    'CERTFR_avis': 'https://www.cert.ssi.gouv.fr/avis/feed/'
}

# Avoid error checking TLS certificate
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context