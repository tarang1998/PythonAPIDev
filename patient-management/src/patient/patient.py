from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.patient.schemas.patient import PatientDataResponse
from src.models.patient import Patient
from flask import abort

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
