from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from app import models

#Blueprint imports and register
from app.routes import property_management_bp, property_search_bp, property_retrieval

bp_property_retrieval = property_retrieval()
app.register_blueprint(bp_property_retrieval)

bp_property_search = property_search_bp()
app.register_blueprint(bp_property_search)

bp_property_management = property_management_bp()
app.register_blueprint(bp_property_management)