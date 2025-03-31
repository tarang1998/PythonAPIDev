from marshmallow import Schema, fields
from src.appointments.schema.appointments import PatientAppointmentDataResponse
from src.medicalhistory.schema.medicalhistory import PatientMedicalHistoryDataResponse

class PatientDataResponse(Schema):

    email = fields.Email(required=True, description="The email address of the patient")
    first_name = fields.Str(required=True, description="The first name of the patient")
    last_name = fields.Str(required=True, description="The last name of the patient")
    dob = fields.Date(required=True, description="The date of birth of the patient in YYYY-MM-DD format")
    appointments = fields.List(fields.Nested(PatientAppointmentDataResponse), description="List of patient's appointments")
    medical_history = fields.List(fields.Nested(PatientMedicalHistoryDataResponse), description="List of patient's medical history")

   

class UpdatePatientData(Schema):
    first_name = fields.Str( description="The first name of the patient")
    last_name = fields.Str( description="The last name of the patient")
    dob = fields.Date(description="The date of birth of the patient in YYYY-MM-DD format")

class UpdatePatientDataResponse(Schema):
    email = fields.Email(required=True, description="The email address of the patient")
    first_name = fields.Str(required=True, description="The first name of the patient")
    last_name = fields.Str(required=True, description="The last name of the patient")
    dob = fields.Date(required=True, description="The date of birth of the patient in YYYY-MM-DD format")


class GetPatientMedicalHistoryResponse(Schema):
    medical_history = fields.List(fields.Nested(PatientMedicalHistoryDataResponse), required = True)


class PostPatientMedicalHistory(Schema):
    diagnosis = fields.Str(required=True)
    medications = fields.Str(required=True)
    allergies = fields.Str(required=True)


class PostPatientMedicalHistoryResponse(Schema):
    id = fields.Integer(required = True)
    diagnosis = fields.Str(required=True)
    medications = fields.Str(required=True)
    allergies = fields.Str(required=True)

class PatchPatientMedicalHistory(Schema):
    diagnosis = fields.Str()
    medications = fields.Str()
    allergies = fields.Str()