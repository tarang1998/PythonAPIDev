from marshmallow import Schema, fields
from src.doctor.schema.doctor import PatientDoctorDataResponse

class PatientMedicalHistoryDataResponse(Schema):
    diagnosis = fields.Str(required=True)
    medications = fields.Str(required=True)
    allergies = fields.Str(required=True)





   

