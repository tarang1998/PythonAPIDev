from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.patient.schemas.patient import PatchPatientMedicalHistory, PatientDataResponse, UpdatePatientData, UpdatePatientDataResponse, GetPatientMedicalHistoryResponse, PostPatientMedicalHistory, PostPatientMedicalHistoryResponse
from src.models.patient import Patient
from src.models.medical_history import MedicalHistory
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


    @patient.response(status_code=204)
    @jwt_required()
    def delete(self):
        
        current_user_id = get_jwt_identity()

        patient_data = Patient.query.filter_by(id = current_user_id).first()

        if not patient_data:
            abort(404, "Patient not found within the system ")

        g.db.delete(patient_data)
        g.db.commit()

        return


@patient.route('/medicalHistory', )
class PatientMedicalHistoryCollection(MethodView):

    @jwt_required()
    @patient.response(status_code=200, schema=GetPatientMedicalHistoryResponse)
    def get(self):
         
        current_user_id = get_jwt_identity()

        patient_data = Patient.query.filter_by(id = current_user_id).first()

        if not patient_data:
            abort(404, "Patient not found within the system ")


        medical_history = MedicalHistory.query.filter_by(patient_id = current_user_id).all()

        return {"medical_history": medical_history}



    @jwt_required()
    @patient.arguments(PostPatientMedicalHistory)
    @patient.response(status_code=201, schema=PostPatientMedicalHistoryResponse)
    def post(self, data):

        current_user_id = get_jwt_identity()

        patient_data = Patient.query.filter_by(id = current_user_id).first()

        if not patient_data:
            abort(404, "Patient not found within the system ")

        medical_data = MedicalHistory(
            diagnosis = data["diagnosis"],
            medications = data["medications"],
            allergies = data["allergies"],
            patient_id = current_user_id  
            )
        
        g.db.add(medical_data)
        g.db.commit()
        return medical_data
    

@patient.route('/medicalHistory/<string:id>')
class PatientIndividualMedicalHistoryCollection(MethodView):

    @jwt_required()
    @patient.response(status_code=200, schema=PostPatientMedicalHistoryResponse)
    def get(self, id):
        current_user_id = get_jwt_identity()

        patient_data = Patient.query.filter_by(id = current_user_id).first()

        if not patient_data:
            abort(404, "Patient not found within the system ")

        medical_history = MedicalHistory.query.filter_by(patient_id = current_user_id, id = id).first()

        if not medical_history:  # You can also use .count() or handle with custom logic
            abort(404, "Medical history record not found")


        return medical_history


    @jwt_required()
    @patient.arguments(PatchPatientMedicalHistory,location="query")
    @patient.response(status_code=201, schema=PostPatientMedicalHistoryResponse)
    def patch(self, params, id):

        current_user_id = get_jwt_identity()

        patient_data = Patient.query.filter_by(id = current_user_id).first()

        if not patient_data:
            abort(404, "Patient not found within the system ")

        medical_history = MedicalHistory.query.filter_by(patient_id = current_user_id, id = id).first()
        
        if not medical_history:  # You can also use .count() or handle with custom logic
            abort(404, "Medical history record not found")

        if "diagnosis" in params:
            medical_history.diagnosis = params["diagnosis"]

        if "medications" in params:
            medical_history.diagnosis = params["diagnosis"]

        if "allergies" in params:
            medical_history.diagnosis = params["diagnosis"]

        g.db.commit()
        return medical_history

    @jwt_required()
    @patient.response(status_code=204)
    def delete(self,id):

        current_user_id = get_jwt_identity()

        patient_data = Patient.query.filter_by(id = current_user_id).first()

        if not patient_data:
            abort(404, "Patient not found within the system ")

        medical_history = MedicalHistory.query.filter_by(patient_id = current_user_id, id = id).first()
        
        if not medical_history:  # You can also use .count() or handle with custom logic
            abort(404, "Medical history record not found")

        g.db.delete(medical_history)
        g.db.commit()

        return
        










    

