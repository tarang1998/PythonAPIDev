from src.database import db

# Availability Model (for doctor schedules)
class Availability(db.Model):

    __tablename__ = 'availabilities'
    
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)

    def __repr__(self):
        return f"<Availability {self.start_time} - {self.end_time}>"