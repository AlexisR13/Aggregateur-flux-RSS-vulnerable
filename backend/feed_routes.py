from flask import request, jsonify, redirect
from flask_jwt_extended import jwt_required, current_user
import feedparser
import json
from html2text import html2text

from config import *
from models import *

# permet de lister tous les feeds disponibles et s'ils sont favoris
@app.route('/', methods=["GET"])
@jwt_required(optional=True)
def show_feeds(): 
    dic = {}
    
    current_identity = current_user
    
    if current_identity:
        
        favorites = current_user.favorites  
        
        feeds = current_user.feeds
                
        defaults = Feed.query.filter_by(default=True).all()
        
        for feed in defaults:
            dic[feed.name] = {"url":feed.url, "id":feed.id, "name":feed.name, "publisher":feed.publisher, "isFavorite":False}  #pas sûr du True, peut-être mettre 0 ou 1
    
        for feed in feeds:
            dic[feed.name] = {"url":feed.url, "id":feed.id, "name":feed.name, "publisher":feed.publisher, "isFavorite":False}  #pas sûr du True, peut-être mettre 0 ou 1
        
        for feed in favorites:
            dic[feed.name] = {"url":feed.url, "id":feed.id, "name":feed.name, "publisher":feed.publisher, "isFavorite":True}  #pas sûr du True, peut-être mettre 0 ou 1
    
    else:
        feeds = Feed.query.filter_by(default=True).all()
            
        for feed in feeds:            
            dic[feed.name] = {"url":feed.url, "id":feed.id, "name":feed.name, "publisher":feed.publisher, "isFavorite":False}
        
    return jsonify(dic)


# Par défaut, cette route renvoie les 50 articles les plus récents
# Il est possible ensuite de changer de page et de nombre d'articles à afficher
# ATTENTION: page indexé à 1
# possible d'appliquer des filtres. Actuellement, que les favoris
@app.route('/articles', methods=["GET"])
@jwt_required(optional=True)
def get_articles():    
    page = request.args.get('page', default = 1, type = int)
    count = request.args.get('count', default =50, type = int)
    feed_id = request.args.get('feed', default = 0, type = int)
    filter = request.args.get('filter', default = "*", type = str)
    current_identity = current_user
    feeds = {}
  
    if filter != "favs" or not current_identity:
        
        if feed_id == 0:  #loading all the feeds
            feeds = json.loads(show_feeds().get_data())
            
        else:  #trying to load a specific feed
            if current_identity:
                #feed = Feed.query.filter_by(id = feed_id, owner_id = current_identity.id).one_or_none()
                feed = current_user.feeds.filter_by(id = feed_id).one_or_none()
                
                if feed is None:                    
                    feed = Feed.query.filter_by(id = feed_id, default=True).one_or_none()
                    
            else:
                feed = Feed.query.filter_by(id = feed_id, default=True).one_or_none()
                            
            rep = False
            if current_identity and feed in current_identity.favorites:
                rep = True
            
            if feed is None:
                return jsonify({"success": False, "message": "Feed not found"})
            
            feeds = {feed.name:{"url":feed.url, "id":feed_id, "isFavorite":rep}}
            
    elif current_identity and filter == "favs":
        
        favorites = current_user.favorites
        
        for feed in favorites:
            feeds[feed.name] = {"url":feed.url, "id":feed.id, "isFavorite":True} 
        
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
def manage_feed(feed_id=0):
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
        feed = Feed.query.filter_by(id = feed_id, owner_id=user_id).first()
        
        if feed is None:
            return jsonify({"success":False, "message":"Feed to delete not found."})
        
        #il faut récupérer le filtre "favs" associé à cet user, et vérifier si le feed y est ou non
        favorites = User.query.with_entities(User.favorites).filter_by(id = user_id).all()

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
    favorites = current_user.favorites
    
    if feed in favorites:
        favorites.remove(feed)
        message = "Feed supprimé des favoris"
    else:
        favorites.append(feed)
        message = "Feed ajouté aux favoris"
        
    db.session.commit()
    return jsonify({"success":True, "message":message})


# pour sauvegarder un article, ou supprimer un article des articles sauvegardés
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