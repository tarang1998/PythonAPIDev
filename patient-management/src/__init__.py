# The __init__.py serves double duty: it will contain the application factory, 
# and it tells Python that the flaskr directory should be treated as a package.

import os
from flask import Flask, g
from config import Config
from src.database import db  # Import the database instance from the database module  
from flask_migrate import Migrate

from src.models.patient import Patient 
from src.models.doctor import Doctor 
from src.models.appointments import Appointment
from src.models.medical_history import MedicalHistory
from src.models.availability import Availability


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
    
    @app.teardown_appcontext
    def teardown(exception):
        if hasattr(g, 'db'):
            # Ensure to remove the session and close it properly
            g.db.remove()  # This will clean up the session and release any resources associated with it
       
    return app