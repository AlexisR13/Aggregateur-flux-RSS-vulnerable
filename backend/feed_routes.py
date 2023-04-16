from flask import request, jsonify, redirect
from flask_jwt_extended import jwt_required, current_user
import feedparser
import json
from html2text import html2text

from config import *
from models import *

#Ajout à cette route la possibilité de lister que les feeds favoris via le paramètre optionnel filter
@app.route('/', methods=["GET"])
@jwt_required(optional=True)
def show_feeds():  #add possibility to use filters
    #OUTPUT: {<FEED_NAME>:{"url":<FEED_URL>, "id":<FEED_ID>, "isFavorite:<Boolean>"}...}
    dic = {}
    
    filter = request.args.get('filter', default = "*", type = str)
    
    current_identity = current_user
    
    if current_identity:
        user_id = current_user.id
        # retrieving a==the user filters
        
        
        favorites = Filter.query.with_entities(Filter.feeds).filter_by(owner_id = user_id, name="favs").all()
        #filters = User.query.filter_by(id = user_id).with_entities(User.filters)  #.all ?
        #favorites = filters.with_entities(Filter.feeds).filter_by(name = "favs").all()
        
        if filter == "*":
            feeds = Feed.query.filter_by(owner_id = user_id).all()
            
            defaults = Feed.query.filter_by(default=True).all()
            #default feeds don't have any owner_id
            
            for feed in favorites:
                dic[feed.name] = {"url":feed.url, "id":feed.id, "name":feed.name, "publisher":feed.publisher, "isFavorite":True}  #pas sûr du True, peut-être mettre 0 ou 1
            
            for feed in feeds.except_(favorites):
                dic[feed.name] = {"url":feed.url, "id":feed.id, "name":feed.name, "publisher":feed.publisher, "isFavorite":False}  #pas sûr du True, peut-être mettre 0 ou 1
                
            for feed in defaults.except_(favorites).except_(feeds):
                dic[feed.name] = {"url":feed.url, "id":feed.id, "name":feed.name, "publisher":feed.publisher, "isFavorite":False}  #pas sûr du True, peut-être mettre 0 ou 1
        
        elif filter == "favs":
            
            for feed in favorites:
                dic[feed.name] = {"url":feed.url, "id":feed.id, "name":feed.name, "publisher":feed.publisher, "isFavorite":True}  #pas sûr du True, peut-être mettre 0 ou 1
            
            
    else:
        feeds = Feed.query.filter_by(default=True).all()
        
    for feed in feeds:            
        dic[feed.name] = {"url":feed.url, "id":feed.id, "name":feed.name, "publisher":feed.publisher, "isFavorite":False}
        
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
    current_identity = current_user
  
    if filter == "*" or not current_identity:
        
        if feed == -1:
            feeds = json.loads(show_feeds().get_data())
        else:
            # on s'en fiche s'il n'appartient pas à la personne qui fait la requête, car URL publique.
            feed = Feed.query.filter_by(id = feed).one_or_none()
            feeds = {feed.name:{"url":feed.url, "id":feed.id, "isFavorite":False}}
            
    elif current_identity and filter == "favs":
        
        user_id = current_user.id
        filtered_feeds = Filter.query.with_entities(Filter.feeds).filter_by(owner_id = user_id, name=filter).all()
        
        for feed in filtered_feeds:  #ON SUPPOSE QUE FILTRE = FAVS
            feeds[feed.name] = {"url":feed.url, "id":feed.id, "isFavorite":True}  #pas sûr du True, peut-être mettre 0 ou 1
        
        
    articles = []
    for feedName in feeds:
        url = feeds[feedName]["url"]
        feed = feedparser.parse(url)
        for entry in feed.entries:
            dic = {"name": feedName, "feed_id":feeds[feedName]["id"], "published_parsed":entry.published_parsed,"link": entry.link, "summary":html2text(entry.summary).replace("\n"," "), "title":entry.title, "published":entry.published} #, "entry": entry}
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
        
        nameAlreadyTaken = Feed.query.filter_by(name = request.json.get('name'), owner_id=user_id).first()  #SHOULD BE UNIQUE
        if nameAlreadyTaken:
            return jsonify({"success":False, "message":"Name already taken."})
        
        urlAlreadyTaken = Feed.query.filter_by(url = request.json.get('url'), owner_id=user_id).first()  #SHOULD BE UNIQUE
        if urlAlreadyTaken:
            return jsonify({"success":False, "message":"URL already taken."})
            
        try:
            feed = Feed(url = request.json.get('url'), name = request.json.get('name'), default = False, owner_id = user_id, publisher = feedparser.parse(request.json.get('url'))["feed"]["title"])

            db.session.add(feed)
            db.session.commit()
        except:
            return redirect('/error/admin_feedback_form_beta'), 500
        else:
            
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
    
    feed.name = request.json.get("name")  
    #peut-être nécessaire de faire une nettoyage ici si ce n'est pas fait sur le front
    #par exemple en faisant un strip de tous les caractères qui ne sont pas alphanumériques ou des espaces
    db.session.commit()
    
    return jsonify({"success":True})


@app.route('/edit_favorite/<int:feed_id>', methods = ["GET"])
@jwt_required()
def edit_favorite(feed_id):
    user_id = current_user.id
    feed = Feed.query.filter_by(id = feed_id, owner_id=user_id).one_or_none()  #SHOULD BE UNIQUE
    
    if feed is None:
        feed = Feed.query.filter_by(id = feed_id, default=True).one_or_none()
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


@app.route('/manage_article', methods = ["POST"])
@app.route('/manage_article/<int:article_id>', methods = ["DELETE"])
@jwt_required()
def manage_article(article_id=-1):
    # user does not necessarily need    
    
    if request.method == "POST":
        # Attention, pas de check que article appartient bien au feed.
        # Nécessite juste de parcourir les articles du feed
        
        #mais on suppose que, étant donné que le user est identifié, il ne fasse pas n'importe quoi
        
        feed_id = request.json.get("feed_id")  
        
        #data linked to article
        published_at = request.json.get("published_parsed")  
        link = request.json.get("link")  
        title = request.json.get("title")  
        summary = request.json.get("summary")          
        #to save article
        
        user_id = current_user.id
        
        feed = Feed.query.filter_by(id = feed_id, owner_id=user_id).one_or_none()  #SHOULD BE UNIQUE
    
        if feed is None:
            feed = Feed.query.filter_by(id = feed_id, default=True).one_or_none()
            if feed is None:
                return jsonify({"success":False, "message":"Ce feed ne fait pas partie de votre liste de feeds."})
        
        alreadySaved = Savedarticle.query.filter_by(owner_id = user_id, link = link, title=title, summary=summary).one_or_none()  #SHOULD BE UNIQUE
        if alreadySaved:
            return jsonify({"success":False, "message":"Article already taken."})
        
        article = Savedarticle(link = link, title=title, summary = summary, feed_id = feed_id, owner_id = user_id, published_at = published_at)
        
        db.session.add(article)
        db.session.commit()


        return jsonify({"success":True})
            
    else:
        user_id = current_user.id
        article = Savedarticle(id = article_id, owner_id = user_id).one_or_none()
        
        if article is None:
            return jsonify({"success":False, "message":"Saved article not found."})
            
        db.session.delete(article)
        db.session.commit()
        
        return jsonify({"success":True})


# lister les articles enregistrés
@app.route('/saved_articles', methods = ["GET"])
@jwt_required()
def saved_articles():
    user_id = current_user.id
    
    articles = Savedarticle.query.filter_by(owner_id = user_id).all()
    
    if articles is None:
        return jsonify({"success":False, "message":"No saved articles found."})
    
    dic = {}
    for article in articles:
        feed = Feed.query.filter_by(owner_id = user_id, id = article.feed_id).one_or_none()
        dic[str(article.id)] = {"link" : article.link,
                                "title":article.title, 
                                "summary" : article.summary, 
                                "published_at" : article.published_at,
                                "saved_at" : article.saved_at}
        if feed is not None:
            dic[str(article.id)]["feed_name"] = feed.name
            dic[str(article.id)]["feed_id"] = article.feed_id
            
        else:  # on garde les articles sauvegardés même si le feed correspondant est supprimé
            dic[str(article.id)]["feed_name"] = "Not found"
            dic[str(article.id)]["feed_id"] = -1
            
    return jsonify(dic)
    
# for filter:
# publisher, title, summary, date, feed name, favorite ?