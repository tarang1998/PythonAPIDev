from marshmallow import Schema, fields

class PatientMedicalHistoryDataResponse(Schema):
    id = fields.Integer(required=True)
    diagnosis = fields.Str(required=True)
    medications = fields.Str(required=True)
    allergies = fields.Str(required=True)





   

