from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import ssl

from flask_jwt_extended import JWTManager
from datetime import timedelta


#Fonctionnalités bonus si on à le temps:

# rendre l'authentification galère avec vérification d'email et captcha.
# mieux gérer l'unicité du username
# éviter les timings attacks
# recommendation de flux à partir de ceux stockés dans la DB
    # en utilisant la similarité des flux favoris, ou encore juste la liste des flux associés au compte


# Il faut créer une table d'association pour les favoris, les articles sauvegardés et aussi les articles abonnés

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'admin123@aV3rySecurePassworth(haha)!'
# L'admin n'a pas compris que ce SECRET_KEY n'était pas la même chose que ses credentials, mais qu'il est bête !

# SQL Database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'  #local database for now
db = SQLAlchemy(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret #9fj82_@ax07_uc], thou shall not find it." 
ACCESS_EXPIRES = timedelta(hours=2)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

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