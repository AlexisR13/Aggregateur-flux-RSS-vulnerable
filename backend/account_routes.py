from config import *
from models import *

from flask import request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required
from hmac import compare_digest
import re

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
        (User.query.filter_by(login=username).first(), 'Username already taken')
        ) if has_error]
    
    if len(errors)>0:
        return jsonify({'success': False, "message":"\n".join(errors)})

    user = User(username,password, email)
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=True)
    
    return jsonify({'success': True})


@app.route('/login', methods=["POST"])
def login():
    username = request.json.get('login')
    password = request.json.get('password').encode()
    user = User.query.filter_by(login=username).first()
    #login with email ?
    
    if user and compare_digest(bcrypt.hashpw(password, user.password), user.password):  #failed connexion
        login_user(user, remember=True)
        return jsonify({'success': True})
        
    return jsonify({'success': False, "message":"Identifiant ou mot de passe incorrect."})



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'success': True})

@app.route('/profile')
@login_required
def profile():
    
    
    # Afficher un menu pour le profil avec plusieurs sous-options:
        # modification de mdp
        # modification d'email
        # suppression du compte/effaçage des données
        # ajout d'un flux RSS
    return redirect(url_for('index'))