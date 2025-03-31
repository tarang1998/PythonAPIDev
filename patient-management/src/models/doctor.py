from src.database import db

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique email for each patient
    password = db.Column(db.String(255), nullable=False)  # Hashed password for security
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    availability = db.relationship('Availability', backref='doctor', lazy=True)

    
    def __repr__(self):
        return f"<Doctor {self.first_name} {self.last_name}>"
