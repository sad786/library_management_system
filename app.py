from flask import Flask
from models import db
from auth import jwt
from routes.admin_routes import admin_bp
from routes.user_routes import user_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
