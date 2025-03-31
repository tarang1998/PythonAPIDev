from src.database import db

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    doctor = db.relationship('Doctor', backref='appointments')

    def __repr__(self):
        return f"<Appointment {self.id} - {self.date}>"