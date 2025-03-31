from marshmallow import Schema, fields
from src.doctor.schema.doctor import PatientDoctorDataResponse

class PatientAppointmentDataResponse(Schema):
    datetime = fields.DateTime(format='iso',required = True)
    doctor =  fields.Nested(PatientDoctorDataResponse, required = True)



   

