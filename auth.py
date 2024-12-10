from flask import request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from models import User

jwt = JWTManager()

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return user
    return None

def generate_token(user):
    token = create_access_token(identity={'id': user.id, 'email': user.email, 'role': user.role})
    return token
