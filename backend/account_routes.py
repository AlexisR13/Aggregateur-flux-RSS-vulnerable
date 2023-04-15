from flask import request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from hmac import compare_digest
import re

from config import *
from models import *


# pour logout
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)


@app.route('/signup', methods=["POST"])
def signup():
    username = request.json.get('login')  #or login ..
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

    user = User(username,password, email)
    filter = Filter(owner_id = user.id, name="favs")  #to store user favorites

    db.session.add(user)
    db.session.add(filter)
    db.session.commit()
    
    access_token = create_access_token(identity=user)
    return jsonify({'success':True, 'access_token':access_token})
    
    """login_user(user, remember=True)
    return jsonify({'success': True})"""


@app.route('/login', methods=["POST"])
def login():
    username = request.json.get('login')
    password = request.json.get('password').encode()
    user = User.query.filter_by(login=username).one_or_none()
    #login with email ?
    
    if user and compare_digest(bcrypt.hashpw(password, user.password), user.password):  #failed connexion
        access_token = create_access_token(identity=user)
        return jsonify({'success':True, 'access_token':access_token})
    
        """login_user(user, remember=True)
        return jsonify({'success': True})"""
        
    return jsonify({'success': False})


@app.route('/logout', methods=["GET"])
@jwt_required() #@login_required
def logout():
    jti = get_raw_jwt()['jti']
    revoked_token = RevokedToken(jti=jti)
    db.session.add(revoked_token)
    db.session.commit()
    #logout_user()
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
@jwt_required() #@login_required
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
    
    