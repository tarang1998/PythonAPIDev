from src.database import db

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique email for each patient
    password = db.Column(db.String(255), nullable=False)  # Hashed password for security
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)  # Date of Birth
    # One to many relationship with MedicalHistory, each patient can have multiple medical records
    medical_history = db.relationship('MedicalHistory', backref='patient', lazy=True)
    # One to many relationship with Appointment, each patient can have multiple appointments
    appointments = db.relationship('Appointment', backref='patient', lazy=True)


    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name}>"