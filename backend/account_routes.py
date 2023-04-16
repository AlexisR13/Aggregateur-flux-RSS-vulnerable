from flask import request, jsonify
from hmac import compare_digest
import re
from datetime import datetime
from datetime import timezone

from config import *
from models import *

from flask import Flask, abort, request, render_template_string
import jinja2, re, hashlib

#Message quand user essaie d'accéder à une page @jwt_required sans avoir de token valide:
# {
#     "msg": "Token has been revoked"
# }

@app.route('/signup', methods=["POST"])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')   #should have password confirmation
    email = request.json.get('email')

    #https://stackoverflow.com/questions/25211924/check-every-condition-in-python-if-else-even-if-one-evaluates-to-true
    errors = [message for (has_error, message) in (
        (len(password)<12, 'Password must be at least 12 characters long.'),
        (re.search(r'[A-Z]', password) is None, 'Password must include upper case letters.'),
        (re.search(r'[a-z]', password) is None, 'Password must include lower case letters.'),
        (re.search(r'\d', password) is None, 'Password must include digits.'),
        (re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is None, 'Invalid email.'),
        (User.query.filter_by(login=username).one_or_none() is not None, 'Username already taken')
        ) if has_error]
    
    if len(errors)>0:
        return jsonify({'success': False, "message":"\n".join(errors)})

    user = User(login = username,password = password, email = email)
    db.session.add(user)
    db.session.commit()
    
    filter = Filter(owner_id = user.id, name="favs")  #to store user favorites    
    db.session.add(filter) 
    db.session.commit()
    
    access_token = create_access_token(identity=user)
    return jsonify({'success':True, 'access_token':access_token})


@app.route('/login', methods=["POST"])
def login():
    username = request.json.get('username')
    password = request.json.get('password').encode()
    user = User.query.filter_by(login=username).one_or_none()
    #login with email ?
    
    if user and compare_digest(bcrypt.hashpw(password, user.password), user.password):  #failed connexion
        access_token = create_access_token(identity=user)
        return jsonify({'success':True, 'access_token':access_token})
        
    return jsonify({'success': False})


# Endpoint for revoking the current users access token. Saved the unique
# identifier (jti) for the JWT into our database.
@app.route("/logout", methods=["DELETE"])
@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify({'success': True})


@app.route('/password', methods=["POST"])
@jwt_required() #@login_required
def change_password():    
    user = current_user
    
    old_pw = request.json.get('old_password')
    new_pw = request.json.get('new_password')
    repeated_pw = request.json.get('repeated_password')

    if new_pw != repeated_pw:
        return jsonify({'success': False, "message": "Les deux nouveaux mots de passe ne correspondent pas."})
    
    if user and compare_digest(bcrypt.hashpw(old_pw, user.password), user.password):  
        errors = [message for (has_error, message) in (
            (len(new_pw)<12, 'Password must be at least 12 characters long.'),
            (re.search(r'[A-Z]', new_pw) is None, 'Password must include upper case letters.'),
            (re.search(r'[a-z]', new_pw) is None, 'Password must include lower case letters.'),
            (re.search(r'\d', new_pw) is None, 'Password must include digits.')
        ) if has_error]
    
        if len(errors)>0:
            return jsonify({'success': False, "message":"\n".join(errors)})

        user.password = bcrypt.hashpw(new_pw.encode(), bcrypt.gensalt())
        db.session.commit()
        return jsonify({'success': True, "message":""})
        
    return jsonify({'success': False, "message": "Mauvais mot de passe courant."})


@app.route('/email', methods=["POST"])
@jwt_required() #@login_required
def change_email():
    user = current_user
    
    new_email = request.json.get('new_email')
    password = request.json.get('password')

    if user and compare_digest(bcrypt.hashpw(password, user.password), user.password):  
        errors = [message for (has_error, message) in (
            (re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', new_email) is None, 'Invalid email.')
        ) if has_error]
    
        if len(errors)>0:
            return jsonify({'success': False, "message":"\n".join(errors)})

        user.email = new_email
        db.session.commit()
        return jsonify({'success': True, "message":""})
        
    return jsonify({'success': False, "message": "Mauvais mot de passe courant."})


@app.errorhandler(500)
@app.route('/error/admin_feedback_form_beta', methods=["GET","POST"]) 
def feedback(e=500):
    
    form = '''<form method="POST" action="/error/admin_feedback_form_beta">
                <label for="summary">Titre:</label><br>
                <input type="text" id="summary" name="summary" required><br>
                <label for="description">Description:</label><br>
                <textarea id="description" name="description" rows="5" cols="50" required></textarea><br>
                <input type="submit" value="Submit">
            </form></br></br>'''
    
    if request.method == "POST":
        
        if "summary" in request.form and "description" in request.form:
            summary = request.form["summary"]
            description = request.form["description"]
            feedback = Feedback(summary = summary, description = description)
            db.session.add(feedback)
            db.session.commit()
    
    comments = Feedback.query.all()
    
    template = '''
        <!DOCTYPE html>
        <html>
          <head>
            <title>Error</title>
          </head>
          <body>
            <h1>Erreur 500</h1>
            <p>Vous pouvez aider l'Admin en lui précisant ce qui a conduit à cette erreur:</p></br></br>'''+form+\
        '''<p>Voici les erreurs signalées précedemment par les autres utilisateurs: si la votre est déjà décrite, veuillez ne pas créer un doublon :)</p></br>'''
            
    for comment in comments:
        
        template += '''<div class="comment" style="border: 1px solid black;padding: 10px;">
            <p class="creation-date">'''+comment.created_at.strftime("%d/%m/%Y, %H:%M:%S")+'''</p>
            <h2 class="summary">'''+comment.summary+'''</h2>
            <p class="description">'''+comment.description+'''</p>
        </div>'''

        #template += '''<div class="comment" style="border: 1px solid black;padding: 10px;">
        #    <p class="creation-date">'''+comment.created_at.strftime("%d/%m/%Y, %H:%M:%S")+'''</p>
        #    <h2 class="summary">'''+re.sub(r'[^a-zA-Z0-9 .]', '', comment.summary)+'''</h2>
        #    <p class="description">'''+re.sub(r'[^a-zA-Z0-9 .]', '', comment.description)+'''</p>
        #</div>'''        
        
        
    template += '''</body></html>'''

    return render_template_string(template)

@app.route('/profile', methods=["GET"])
@jwt_required() #@login_required
def profile():
    user = current_user
    if user:
        return jsonify({"id": user.id, "login": user.login, "email": user.email, "created_at":user.created_at})
    else:
        return jsonify({'success': False, "message": "Utilisateur non trouvé."})
    # retrieving a==the user filters
    
    favorites = Filter.query.with_entities(Filter.feeds).filter_by(owner_id = user_id, name="favs").all()
    #filters = User.query.filter_by(id = user_id).with_entities(User.filters)  #.all ?
    #favorites = filters.with_entities(Filter.feeds).filter_by(name = "favs").all()
    feeds = Feed.query.filter_by(owner_id = user_id).all()
    
 
@app.route('/suppress_account', methods=["GET"])
@jwt_required()
def suppress_account():
    user = current_user
    db.session.delete(user)
    
    # pas sûr qu'il soit nécessaire de supprimer séparemment les filtres et feeds, 
    # mais autant le faire dans le doute
    filters = Filter.query.filter_by(owner_id = user.id).all()  
    db.session.delete(filters)
    
    feeds = Feed.query.filter_by(owner_id = user.id).all()
    db.session.delete(feeds)
    
    db.session.commit()
    return jsonify({'success': True, "message":""})
    
    
### NE PAS OUBLIER DE SUPPRIMER CA AVANT DE DOCKERISER ###
@app.route('/show_database_secret_path', methods=["GET"])
def return_db():
    list = {"feeds":[],"filters":[],"users":[]}
    filters = Filter.query.all()
    feeds = Feed.query.all()
    users = User.query.all()
    for feed in feeds:
        list["feeds"].append(str(feed))
    for filter in filters:
        list["filters"].append(str(filter))
    for user in users:
        list["users"].append(str(user))
    return jsonify(list)