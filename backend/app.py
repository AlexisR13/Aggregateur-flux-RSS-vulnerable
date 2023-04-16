import os

from config import *
from models import *
from feed_routes import *
from account_routes import *

if __name__ == "__main__":
    
    with app.app_context():
        
        db.drop_all() #FOR TESTING PURPOSES ONLY
        
        db.create_all()
        
        default_feeds = []
        
        for key in FEEDS:
            url=FEEDS[key]
            try:
                publisher = feedparser.parse(url)["feed"]["title"]
            except:
                publisher = ""
            default_feeds.append(Feed(name=key, url=url, default=True, publisher = ""))
            
        db.session.add_all(default_feeds)
        
        admin = User("admin","aV3rySecurePassworth(haha)!", "193892fjzfizj00@gmail.com")
        db.session.add(admin)
        
        db.session.commit()

    # Listen on docker inside networks interface (or localhost if use without docker)
    app.run(port=5000, host=os.environ.get('LISTENING_INTERFACE'), debug=True)