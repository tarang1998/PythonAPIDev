from flask_sqlalchemy import SQLAlchemy
import string
import random

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    upadated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)
    bookmarks = db.relationship('Bookmarks', backref='user', lazy=True)  # One-to-many relationship with Bookmarks

    def __repr__(self):
        return f"<User {self.id}/{self.username}>"
    

    
class Bookmarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)  # Optional field for additional notes or tags
    url = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    visits = db.Column(db.Integer, default=0, nullable=False)  # Track the number of visits to the bookmark
    short_url = db.Column(db.String(3), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

    def __repr__(self):
        return f"<Bookmark {self.id}/{self.title}>"
    
    def generate_short_characters(self):
        characters = string.digits + string.ascii_letters  # Include digits and letters for the short URL
        picked = ''.join(random.choice(characters) for _ in range(3))  # Generate a random 3-character string
    
        link = self.query.filter_by(short_url=picked).first()
        if link:
            # If the generated short URL already exists, generate a new one recursively
            return self.generate_short_characters()
        return picked
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_characters()  # Generate a short URL when creating a new bookmark