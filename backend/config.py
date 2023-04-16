from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import ssl

from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'Hehi#h838Fc8d_iaU%@cDc'

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
    'CERTFR avis': 'https://www.cert.ssi.gouv.fr/avis/feed/',
    'CISA Alerts': 'https://www.us-cert.gov/ncas/alerts',
    
    'DarkNet': 'http://feeds.feedburner.com/darknethackers',

    'InfoSecurity Mag': 'http://www.infosecurity-magazine.com/rss/news/',

    'Krebs on Security': 'http://krebsonsecurity.com/feed/',

    'Naked Security': 'http://nakedsecurity.sophos.com/feed/',

    'ThreatPost': 'http://threatpost.com/feed/'
}

# Avoid error checking TLS certificate
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context
    
    """
"""