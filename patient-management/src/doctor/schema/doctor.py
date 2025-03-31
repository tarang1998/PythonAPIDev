from marshmallow import Schema, fields


class PatientDoctorDataResponse(Schema):
    email = fields.Email(required=True, description="The email address of the new user")
    first_name = fields.Str(required=True, description="The first name of the new user")
    last_name = fields.Str(required=True, description="The last name of the new user")


   



