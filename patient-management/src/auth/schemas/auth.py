from marshmallow import Schema, fields, validates, ValidationError
import re

def validate_email_format(email):
    # Example: Custom regex for email format validation (you can modify this)
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(email_regex, email):
        raise ValidationError("Please provide a valid email address.")

class RegisterPatient(Schema):

    email = fields.Email(required=True, description="The email address of the new user")
    password = fields.Str(required=True, description="The password for the new user", load_only=True)
    first_name = fields.Str(required=True, description="The first name of the new user")
    last_name = fields.Str(required=True, description="The last name of the new user")
    dob = fields.Date(required=True, description="The date of birth of the new user in YYYY-MM-DD format")

    # Custom validation for email (checks for existing email)
    @validates('email')
    def validate_email(self, value):
        validate_email_format(value)  # Check if the email already exists in the database


class RegisterDoctor(Schema):
    email = fields.Email(required=True, description="The email address of the new user")
    password = fields.Str(required=True, description="The password for the new user", load_only=True)
    first_name = fields.Str(required=True, description="The first name of the new user")
    last_name = fields.Str(required=True, description="The last name of the new user")
    specialty = fields.Str(required=True, description="The specialty of the doctor")  # e.g., cardiology, dermatology, etc.

class RegisterUserResponse(Schema):
    access_token = fields.Str(required=True, description="JWT access token for the authenticated user")
    refresh_token = fields.Str(required=True, description="JWT refresh token for the authenticated user")


class LoginUser(Schema):
    email = fields.Email(required=True, description="The email address of the new user")
    password = fields.Str(required=True, description="The password for the new user", load_only=True)

class LoginResponse(Schema):
    access_token = fields.Str(required=True, description="JWT access token for the authenticated user")
    refresh_token = fields.Str(required=True, description="JWT refresh token for the authenticated user")
