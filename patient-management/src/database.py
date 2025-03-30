from flask_sqlalchemy import SQLAlchemy
from flask import current_app, g


db = SQLAlchemy()


# Function to get the DB session
def get_db_session():
    if 'db' not in g:
        g.db = db.session
    return g.db


