from flask import Flask
from flask_cors import CORS
import feedparser
import ssl

app = Flask(__name__)
CORS(app)

# Avoid error checking TLS certificate
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


FEEDS = {
    # 'feed_name' : 'feed_url',
    'ANSSI_publications': 'http://www.ssi.gouv.fr/feed/publication/',
    'ANSSI_actualites': 'https://www.ssi.gouv.fr/feed/actualite/',
    'CERTFR_alertes': 'https://www.cert.ssi.gouv.fr/alerte/feed/',
    'CERTFR_menaces_et_incidents': 'https://www.cert.ssi.gouv.fr/cti/feed/',
    'CERTFR_avis': 'https://www.cert.ssi.gouv.fr/avis/feed/'
}

@app.route('/')
def show_feeds():
   return FEEDS

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
  app.run(port=5000, debug=True)