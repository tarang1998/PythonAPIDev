from . import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True,nullable=False,) 
    lastname = db.Column(db.String(200), unique=True, nullable=False)
    firstname = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    funds = db.relationship('Fund', backref='user')


    def __repr__(self):
        return f'<User: {self.id} {self.email}>'
    
class Fund(db.Model):
    __tablename__ = 'funds'
    id = db.Column(db.Integer, primary_key=True,nullable=False,)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'amount': str(self.amount),
            'user_id': self.user_id,
            'created_at': self.created_at
        }