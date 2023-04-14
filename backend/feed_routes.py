from config import *
from models import *


#Il faudrait avoir une vue un peu comme dans gmail, avec une liste limitée de flux.
#Avec un bouton  "en savoir plus", ça serait top si on peut afficher directement dans le navigateur le contenu de la page web

@app.route('/', methods=["GET"])
def show_feeds():
    #OUTPUT: {<FEED_NAME>:{"url":<FEED_URL>, "id":<FEED_ID>, "isFavorite:<Boolean>"}...}
    dic = {}
    
    if current_user.is_authenticated:
        user_id = int(current_user.get_id())
        # retrieving a==the user filters
        
        favorites = Filter.query.with_entities(Filter.feeds).filter_by(owner_id = user_id, name="favs").all()
        #filters = User.query.filter_by(id = user_id).with_entities(User.filters)  #.all ?
        #favorites = filters.with_entities(Filter.feeds).filter_by(name = "favs").all()
        feeds = Feed.query.filter_by(owner_id = user_id).all()
        
        for feed in favorites:
            dic[feed.name] = {"url":feed.url, "id":feed.id, "isFavorite":True}  #pas sûr du True, peut-être mettre 0 ou 1
        
        for feed in feeds.except_(favorites):
            dic[feed.name] = {"url":feed.url, "id":feed.id, "isFavorite":False}  #pas sûr du True, peut-être mettre 0 ou 1
    else:
        feeds = Feed.query.filter_by(default=True).all()
        
    for feed in feeds:            
        dic[feed.name] = {"url":feed.url, "id":feed.id, "isFavorite":False}
        
    return jsonify(dic)
#retourner aussi tous les IDs de filtres ?

#aussi à implémenter: la création d'un filtre favoris pour chaque user
# profile public ou non
# avec amis pour recommendations

# search users pour ajouter les utilisateurs

#utilisateurs peuven partager ou non leur flux, partager ou non leur feeds subscribed

#les recommendations ? JSP 


# Par défaut, cette route renvoie les 50 articles les plus récents
# Il est possible ensuite de changer de page et de nombre d'articles à afficher
# ATTENTION: page indexé à 1
@app.route('/articles', methods=["GET"])
@app.route('/articles/<int:page>', methods=["GET"])
@app.route('/articles/<int:page>/<int:count>', methods=["GET"])
def get_articles(page=1, count=50):
    # prend en input l'output de "/": OUTPUT: {<FEED_NAME>:{"url":<FEED_URL>, "isFavorite:<Boolean>"}...}
    # le isFavorite n'est ici pas utilisé
    # retourne: l'objet feedparse qui stocke tous les articles, jsonifié
    
    feeds = request.form['feeds']
    
    articles = []
    for feedName in feeds:
        url = feedName["url"]
        feed = feedparser.parse(url)
        articles.extend(feed.entries)
        
    articles.sort(key= lambda entry:entry.published_parsed, reverse=True)
    
    return jsonify(articles[(page-1)*count:page*count])
       
       
@app.route('/manage_feed', methods = ["POST"])
@app.route('/manage_feed/<int:feed_id>', methods = ["DELETE"])
@login_required
def manage_feed(feed_id=-1):
    # On suppose que pour le delete, on a en entrée l'ID du filtre
    # Mais on pourrait facilement adapter la fonction si on a juste le nom du feed (en utilisant alors le user_id)
    # On impose que chaque nom de feed est unique (pour un user donné)
    
    if request.method == "POST":
        user_id = int(current_user.get_id())
        
        alreadyTaken = Feed.query.filter_by(name = request.form['name'], owner_id=user_id).first()  #SHOULD BE UNIQUE
        if alreadyTaken:
            return jsonify({"success":False})
            
        feed = Feed(url = request.form['url'], name = request.form['name'], default = False, owner_id = user_id)

        db.session.add(feed)
        db.session.commit()
        
        return jsonify({"success":True})
            
    else:
        user_id = int(current_user.get_id())
        feed = Feed.query.filter_by(id = feed_id, owner_id=user_id).first()  #SHOULD BE UNIQUE
        
        if feed is None:
            return jsonify({"success":False})
            
        db.session.delete(feed)
        db.session.commit()
        
        return jsonify({"success":True})

    
@app.route('/rename_feed/<int:feed_id>', methods = ["POST"])
@login_required
def rename_feed(feed_id):
    
    user_id = int(current_user.get_id())
    feed = Feed.query.filter_by(id = feed_id, owner_id=user_id).first()  #SHOULD BE UNIQUE
    
    if feed is None:
        return jsonify({"success":False})
    
    feed.name = request.form["name"]   
    #peut-être nécessaire de faire une nettoyage ici si ce n'est pas fait sur le front
    #par exemple en faisant un strip de tous les caractères qui ne sont pas alphanumériques ou des espaces
    db.session.commit()
    
    return jsonify({"success":True})


@app.route('/edit_favorite/<int:feed_id>', methods = ["GET"])
@login_required
def edit_favorite(feed_id):
    user_id = int(current_user.get_id())
    feed = Feed.query.filter_by(id = feed_id, owner_id=user_id).first()  #SHOULD BE UNIQUE
    
    if feed is None:
        return jsonify({"success":False})
    
    #il faut récupérer le filtre "favs" associé à cet user, et vérifier si le feed y est ou non
    favorites = Filter.query.with_entities(Filter.feeds).filter_by(owner_id = user_id, name="favs").all()
    
    if favorites.query.filter_by(id = feed_id).exists():
        favorites.feeds.remove(feed)
    else:
        favorites.feeds.append(feed)

    db.session.commit()
    return jsonify({"success":True})


@app.route('/preview', methods=["POST"])
def article_preview():
    url = request.json.get('url')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        title = soup.find('title').string
        desc = soup.find('meta',attrs = {'name':'description'})['content']
        image = soup.find('meta', property='og:image')['content']
    except:
        return jsonify({'success': False, "message": "Problème lors de la récupération des données du site."})
    else:        
        return jsonify({'title':title,'description':desc,'image':image})
    
@app.route('/bigpreview', methods=["POST"])
def article_bigpreview():
    url = request.json.get('url')
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser').select('body > main')
    
    return str(soup)
    try:
        title = soup.find('title').string
        desc = soup.find('meta',attrs = {'name':'description'})['content']
        image = soup.find('meta', property='og:image')['content']
    except:
        return jsonify({'success': False, "message": "Problème lors de la récupération des données du site."})
    else:        
        return jsonify({'title':title,'description':desc,'image':image})
    
    
    
@app.route('/content', methods=["POST"])
def get_content():
    url = request.json.get('url')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Remove unwanted elements such as ads, scripts, CSS and headers
    for script in soup(["script", "style", "link", "meta"]):
        script.extract()

    # Get the simplified view content
    simplified_view_content = soup.get_text()
    
    return simplified_view_content
    # Return the data as a JSON object
    return jsonify({
        'titles': titles,
        'text': text
    })