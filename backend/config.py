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
    'CISA Current Activity': 'https://www.us-cert.gov/ncas/current-activity',
    'NCSC Report Feed': 'https://www.ncsc.gov.uk/api/1/services/v1/report-rss-feed',
    'Latest threat advice': 'https://www.cyber.gov.au/rssfeed/2',
    'Center for Internet Security': 'https://www.cisecurity.org/feed/advisories',
    'NIST':'https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss-analyzed.xml',
    'Vmware': 'https://www.vmware.com/security/advisories.xml',
    'US-cert': 'https://us-cert.cisa.gov/ncas/alerts.xml',
    'Us-cert weekly': 'https://us-cert.cisa.gov/ncas/bulletins.xml',
    'Naked Security': 'https://www.nakedsecurity.sophos.com/feed '
}

# Avoid error checking TLS certificate
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context