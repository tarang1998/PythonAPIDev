# The __init__.py serves double duty: it will contain the application factory, 
# and it tells Python that the flaskr directory should be treated as a package.

import os
from flask import Flask, g, jsonify
from config import Config
from src.database import db, get_db_session  # Import the database instance from the database module  
from flask_migrate import Migrate
from flask_smorest import Api
from src.models.patient import Patient 
from src.models.doctor import Doctor 
from src.models.appointments import Appointment
from src.models.medical_history import MedicalHistory
from src.models.availability import Availability
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException



from src.auth.auth import auth as auth_blueprint  # Import the auth blueprint


def create_app():
    

    # instance_relative_config=True tells the app that configuration files are relative to the instance folder. 
    # The instance folder is located outside the src package
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_object(Config)



    @app.route('/')
    def index():
        return 'Patient Management System APIs'
    
    db.init_app(app)  # Initialize the database with the app
    migrate = Migrate(app, db)
    JWTManager(app)

    api = Api(app)  # Create an API instance with the Flask app 
    api.register_blueprint(auth_blueprint)



    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Customize the error response to include the description."""
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "message": e.description
        }).data
        response.content_type = "application/json"
        return response
    
    # Setup before_request to ensure db session is set up
    @app.before_request
    def before_request():
        # Ensure that the session is available globally
        get_db_session()

    @app.teardown_appcontext
    def teardown(exception):
        if hasattr(g, 'db'):
            # Ensure to remove the session and close it properly
            g.db.remove()  # This will clean up the session and release any resources associated with it
       
    return app