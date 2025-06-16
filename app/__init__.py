from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
db = SQLAlchemy(app)

from app import models

#Blueprint imports and register
from app.routes import property_management_bp, property_search_bp, property_retrieval, JWT_auth_bp

for bp in [property_retrieval(), property_search_bp(), property_management_bp(), JWT_auth_bp()]:
    app.register_blueprint(bp)