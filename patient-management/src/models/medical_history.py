from src.database import db



# Medical History Model (for patient medical records)
class MedicalHistory(db.Model):
    __tablename__ = 'medical_histories'
    
    id = db.Column(db.Integer, primary_key=True)
    diagnosis = db.Column(db.String(255))
    medications = db.Column(db.String(255))
    allergies = db.Column(db.String(255))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)

    def __repr__(self):
        return f"<MedicalHistory {self.diagnosis}>"