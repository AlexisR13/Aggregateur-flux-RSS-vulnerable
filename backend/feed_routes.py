from flask import request, jsonify
from flask_login import current_user, login_required
from bs4 import BeautifulSoup
import feedparser
import requests
import json

from config import *
from models import *


#Il faudrait avoir une vue un peu comme dans gmail, avec une liste limitée de flux.
#Avec un bouton  "en savoir plus", ça serait top si on peut afficher directement dans le navigateur le contenu de la page web

@app.route('/', methods=["GET"])
@jwt_required(optional=True)
def show_feeds():
    #OUTPUT: {<FEED_NAME>:{"url":<FEED_URL>, "id":<FEED_ID>, "isFavorite:<Boolean>"}...}
    dic = {}
    
    current_identity = get_jwt_identity()
    
    if current_identity:
        user_id = current_user.id
        # retrieving a==the user filters
        
        favorites = Filter.query.with_entities(Filter.feeds).filter_by(owner_id = user_id, name="favs").all()
        #filters = User.query.filter_by(id = user_id).with_entities(User.filters)  #.all ?
        #favorites = filters.with_entities(Filter.feeds).filter_by(name = "favs").all()
        feeds = Feed.query.filter_by(owner_id = user_id).all()
        
        defaults = Feed.query.filter_by(default=True).all()
        
        for feed in favorites:
            dic[feed.name] = {"url":feed.url, "id":feed.id, "isFavorite":True}  #pas sûr du True, peut-être mettre 0 ou 1
        
        for feed in feeds.except_(favorites):
            dic[feed.name] = {"url":feed.url, "id":feed.id, "isFavorite":False}  #pas sûr du True, peut-être mettre 0 ou 1
            
        for feed in defaults.except_(favorites).except_(feeds):
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
@jwt_required(optional=True)
def get_articles():
    # prend en input l'output de "/": OUTPUT: {<FEED_NAME>:{"url":<FEED_URL>, "isFavorite:<Boolean>"}...}
    # le isFavorite n'est ici pas utilisé
    # retourne: l'objet feedparse qui stocke tous les articles, jsonifié
    
    page = request.args.get('page', default = 1, type = int)
    count = request.args.get('count', default =50, type = int)
    feed = request.args.get('feed', default = -1, type = int)
    filter = request.args.get('filter', default = "*", type = str)
    current_identity = get_jwt_identity()
  
    if filter == "*" or not current_identity:
        
        if feed == -1:
            feeds = json.loads(show_feeds().get_data())
        else:
            # on s'en fiche s'il n'appartient pas à la personne qui fait la requête, car URL publique.
            feed = Feed.query.filter_by(id = feed).one_or_none()
            feeds = {feed.name:{"url":feed.url, "id":feed.id, "isFavorite":False}}
            
    elif current_identity and filter != "*":
        
        user_id = current_user.id
        filtered_feeds = Filter.query.with_entities(Filter.feeds).filter_by(owner_id = user_id, name=filter).all()
        
        for feed in filtered_feeds:  #ON SUPPOSE QUE FILTRE = FAVS
            feeds[feed.name] = {"url":feed.url, "id":feed.id, "isFavorite":True}  #pas sûr du True, peut-être mettre 0 ou 1
        
        
    articles = []
    for feedName in feeds:
        url = feeds[feedName]["url"]
        feed = feedparser.parse(url)
        for entry in feed.entries:
            dic = {"name": feedName, "published_parsed":entry.published_parsed,"link": entry.link, "summary":entry.summary, "title":entry.title, "published":entry.published}
            articles.append(dic)
        
    articles.sort(key= lambda entry:entry["published_parsed"], reverse=True)
    
    return jsonify(articles[(page-1)*count:page*count])
       
       
@app.route('/manage_feed', methods = ["POST"])
@app.route('/manage_feed/<int:feed_id>', methods = ["DELETE"])
@jwt_required()
def manage_feed(feed_id=-1):
    # On suppose que pour le delete, on a en entrée l'ID du filtre
    # Mais on pourrait facilement adapter la fonction si on a juste le nom du feed (en utilisant alors le user_id)
    # On impose que chaque nom de feed est unique (pour un user donné)
    
    if request.method == "POST":
        user_id = current_user.id
        
        nameAlreadyTaken = Feed.query.filter_by(name = request.json.get['name'], owner_id=user_id).first()  #SHOULD BE UNIQUE
        if nameAlreadyTaken:
            return jsonify({"success":False, "message":"Name already taken."})
        
        urlAlreadyTaken = Feed.query.filter_by(url = request.json.get['url'], owner_id=user_id).first()  #SHOULD BE UNIQUE
        if urlAlreadyTaken:
            return jsonify({"success":False, "message":"URL already taken."})
            
        feed = Feed(url = request.form['url'], name = request.form['name'], default = False, owner_id = user_id)

        db.session.add(feed)
        db.session.commit()
        
        return jsonify({"success":True})
            
    else:
        user_id = current_user.id
        feed = Feed.query.filter_by(id = feed_id, owner_id=user_id).first()  #SHOULD BE UNIQUE
        
        if feed is None:
            return jsonify({"success":False})
        
        #il faut récupérer le filtre "favs" associé à cet user, et vérifier si le feed y est ou non
        favorites = Filter.query.with_entities(Filter.feeds).filter_by(owner_id = user_id, name="favs").all()

        if favorites.query.filter_by(id = feed_id).exists():
            favorites.feeds.remove(feed)
            
        db.session.delete(feed)
        db.session.commit()
        
        return jsonify({"success":True})

    
@app.route('/rename_feed/<int:feed_id>', methods = ["POST"])
@jwt_required()
def rename_feed(feed_id):
    
    user_id = current_user.id
    feed = Feed.query.filter_by(id = feed_id, owner_id=user_id).first()  #SHOULD BE UNIQUE
    
    if feed is None:
        return jsonify({"success":False})
    
    feed.name = request.json.get["name"]   
    #peut-être nécessaire de faire une nettoyage ici si ce n'est pas fait sur le front
    #par exemple en faisant un strip de tous les caractères qui ne sont pas alphanumériques ou des espaces
    db.session.commit()
    
    return jsonify({"success":True})


@app.route('/edit_favorite/<int:feed_id>', methods = ["GET"])
@jwt_required()
def edit_favorite(feed_id):
    user_id = current_user.id
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