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
    'anssi_publications': 'http://www.ssi.gouv.fr/feed/publication/',
    'anssi_actualites': 'https://www.ssi.gouv.fr/feed/actualite/'
}

@app.route('/')
def show_feeds():
   return FEEDS

@app.route('/<feed_name>')
def get_feed(feed_name):
    feed_url = FEEDS[feed_name]
    feed = feedparser.parse(feed_url)
    first_article = feed['entries'][0]
    return first_article

if __name__ == "__main__":
  app.run(port=5000, debug=True)