import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler

from app.data_processing.data_processing import DataProcessing


app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
db = SQLAlchemy(app)





from app import models

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        with app.app_context():
            background_operation = BackgroundScheduler()
            background_operation.add_job(DataProcessing.data_processing, 'interval', seconds=5, args=[db, models, app], max_instances=1)
            background_operation.start()

#Blueprint imports and register
from app.routes import property_management_bp, property_search_bp, property_retrieval, JWT_auth_bp

for bp in [property_retrieval(), property_search_bp(), property_management_bp(), JWT_auth_bp()]:
    app.register_blueprint(bp)