from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.patient.schemas.patient import PatientDataResponse, UpdatePatientData, UpdatePatientDataResponse
from src.models.patient import Patient
from flask import abort,g 
import datetime

patient = Blueprint("Patient", "Patient",url_prefix='/api/v1/patient', description='Patient Operations',)


@patient.route('/', )
class PatientCollection(MethodView):

    @jwt_required()
    @patient.response(status_code=200,schema=PatientDataResponse)
    def get(self):

        current_user_id = get_jwt_identity()

        patient_data = Patient.query.filter_by(id = current_user_id).first()

        if not patient_data:
            abort(404, "Patient not found within the system ")

        return patient_data
    
    @patient.arguments(UpdatePatientData)
    @patient.response(schema = UpdatePatientDataResponse, status_code=200)
    @jwt_required()
    def patch(self, data):
        current_user_id = get_jwt_identity()

        patient_data = Patient.query.filter_by(id = current_user_id).first()

        if not patient_data:
            abort(404, "Patient not found within the system ")

        # Update patient fields if the data is provided
        if 'first_name' in data:
            patient_data.first_name = data['first_name']
        
        if 'last_name' in data:
            patient_data.last_name = data['last_name']
        
        if 'dob' in data:
            patient_data.dob = data['dob']

        g.db.commit()
        
        return patient_data








    

