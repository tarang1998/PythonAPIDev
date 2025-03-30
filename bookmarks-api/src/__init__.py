
from flask import Flask, abort, jsonify, redirect
import os 
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db, Bookmarks
from flask_jwt_extended import JWTManager
from constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY = os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI'),  # Default to SQLite if not set
            JWT_SECRET_KEY = "your_jwt_secret_key",  # Replace with your actual JWT secret key
            SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable track modifications to avoid warnings
        )
    
    else:
        app.config.from_mapping(test_config)

    @app.get("/")
    def index():
        return jsonify(message="Welcome to the Bookmarks API!")
    


    db.init_app(app)  # Initialize the database with the app

    JWTManager(app)

    app.register_blueprint(auth)  # Register the auth blueprint 
    app.register_blueprint(bookmarks)  # Register the bookmarks blueprint

    @app.get('/<short_url>')
    def redirect_to_url(short_url):
        bookmark = Bookmarks.query.filter_by(short_url=short_url).first_or_404()

        if bookmark:
            bookmark.visits = bookmark.visits+1
            db.session.commit()
            return redirect(bookmark.url)
        
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR

        
    return app

