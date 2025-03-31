from flask_smorest import Blueprint
from flask.views import MethodView
from src.auth.schemas.auth import LoginUser, RegisterUserResponse, LoginResponse, RegisterPatient, RegisterDoctor
from flask import abort,g
from src.models.patient import Patient
from src.models.doctor import Doctor  
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint(
    'Authentication', 
    "auth", 
    url_prefix='/auth', 
    description='Auth operations')

def generate_tokens(user_id):
    identity = str(user_id)
    refresh = create_refresh_token(identity=identity)
    access = create_access_token(identity=identity)
    return refresh, access


@auth.post('/registerPatient', )
@auth.arguments(RegisterPatient)
@auth.response(status_code=201,schema=RegisterUserResponse)
def register(new_patient):
    print("Registering the patient")

    user = g.db.query(Patient).filter(Patient.email == new_patient["email"]).first()
    if user is not None:
        print("Email already exists")
        abort(code = 409, description="The provided email already exists",)

    pwd_hash = generate_password_hash(new_patient["password"])

    patient = Patient(
        email=new_patient["email"],
        password=pwd_hash,  # You should hash the password in a real application
        first_name=new_patient["first_name"],
        last_name=new_patient["last_name"],
        dob=new_patient["dob"]
    )

    try:
        g.db.add(patient)
        g.db.commit()
    except Exception as e:
        print("An error occurred while creating the patient:", e)
        g.db.rollback()
        abort(500, description=f"An error occurred while creating the patient")

    refresh_token, access_token = generate_tokens(patient.id)
    print(refresh_token, access_token)
    print("User registered successfully")

    return {"access_token": access_token, "refresh_token": refresh_token}



@auth.post('/registerDoctor',)
@auth.arguments(RegisterDoctor)
@auth.response(status_code=201,schema=RegisterUserResponse)
def register(new_doctor):
    print("Registering the doctor")

    user = g.db.query(Doctor).filter(Patient.email == new_doctor["email"]).first()
    if user is not None:
        print("Email already exists")
        abort(code = 409, description="The provided email already exists",)

    pwd_hash = generate_password_hash(new_doctor["password"])

    doctor = Doctor(
        email=new_doctor["email"],
        password=pwd_hash,  # You should hash the password in a real application
        first_name=new_doctor["first_name"],
        last_name=new_doctor["last_name"],
        specialty = new_doctor["specialty"],  # Specialty is required for doctors
    )

    try:
        g.db.add(doctor)
        g.db.commit()
    except Exception as e:
        print("An error occurred while creating the doctor:", e)
        g.db.rollback()
        abort(500, description=f"An error occurred while creating the patient")

    refresh_token, access_token = generate_tokens(doctor.id)
    print(refresh_token, access_token)
    print("Doctor registered successfully")

    return {"access_token": access_token, "refresh_token": refresh_token}

        



@auth.post('/login',)
@auth.arguments(LoginUser)
@auth.response(status_code=200,schema=LoginResponse)
def login(user_data):

    # First check if username exists in patients table
    patient = Patient.query.filter_by(email=user_data["email"]).first()
    
    # Then check if username exists in doctors table
    doctor = Doctor.query.filter_by(email=user_data["email"]).first()

    # Verify password for patient or doctor
    user = None
    password = user_data["password"]

    if patient:
        user = patient
    elif doctor:
        user = doctor
    else:
        abort(404, description="User with the provided email does not exist")

    is_pass_correct = check_password_hash(user.password, password)

    if is_pass_correct:
        refresh_token, access_token = generate_tokens(user.id)
        return {"access_token": access_token, "refresh_token": refresh_token}


    else:
        print("Incorrect incorrect Credentials")
        abort(401, description="Incorrect password")

 
@auth.get('/token/refresh', )
@jwt_required(refresh=True)
def refresh_users_token():

    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)

    return ({
        'access_token': access_token
    }), 200



