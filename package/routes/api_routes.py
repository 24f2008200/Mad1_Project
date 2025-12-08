# Hospital Management REST API Routes

from flask import Blueprint, jsonify, request, send_from_directory
from flask_restful import Api, Resource
from flask_login import current_user
from package.routes.auth import login_or_token_required, admin_required, doctor_required, patient_required
from package.routes.utils import get_appointment_rows
from models import db, Doctor, Appointment, User, Patient, Department,AppointmentStatus
from datetime import datetime

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

# ---------------- JSON ENFORCER ---------------- #
def get_json_data():
    if not request.is_json:
        return None, {"error": "Content-Type must be application/json"}, 415
    data = request.get_json(silent=True)
    if data is None:
        return None, {"error": "Invalid or malformed JSON"}, 400
    return data, None


# ----------------------------------------------------------------------------- #
class DoctorResource(Resource):

    @login_or_token_required
    def get(self, doctor_id=None):
        if doctor_id:
            d = Doctor.query.get_or_404(doctor_id)
            return {
                "id": d.id,
                "name": f"{d.name} {d.last_name}",
                "email": d.email,
                "department": d.department.name if d.department else None,
                "phone": d.phone,
                "experience": d.experience,
                "status": d.status
            }, 200

        doctors = Doctor.query.filter(Doctor.status != "deleted").all()
        return [
            {
                "id": d.id,
                "name": f"{d.name} {d.last_name}",
                "email": d.email,
                "department": d.department.name if d.department else None,
                "status": d.status
            } for d in doctors
        ], 200

    
    @admin_required
    def post(self):
        print("here")
        data, error = get_json_data()
        if error: return error

        if "name" not in data or "email" not in data:
            return {"error": "Name and email required"}, 400
        dob_str = data.get("dob")   
        doctor = Doctor(
            name=data["name"],
            last_name=data.get("last_name", ""),
            email=data["email"],
            dob =datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None,
            phone=data.get("phone"),
            license_number=data.get("license_number"),
            experience=data.get("experience"),
            department_id=data.get("department_id"),
            password=data.get("password", "defaultpass"),
            status="active",
        )
        db.session.add(doctor)
        try:
            db.session.commit()
            return {"message": "Doctor created", "id": doctor.id}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500


    @admin_required
    def put(self, doctor_id):
        doctor = Doctor.query.get_or_404(doctor_id)
        data, error = get_json_data()
        if error: return error

        doctor.name = data.get("name", doctor.name)
        doctor.last_name = data.get("last_name", doctor.last_name)
        doctor.phone = data.get("phone", doctor.phone)
        doctor.status = data.get("status", doctor.status)
        db.session.commit()
        return {"message": "Doctor updated"}, 200

    @admin_required
    def delete(self, doctor_id):
        doctor = Doctor.query.get_or_404(doctor_id)
        doctor.status = "deleted"
        db.session.commit()
        return {"message": "Doctor deleted"}, 200


# ----------------------------------------------------------------------------- #
class AppointmentResource(Resource):

    @login_or_token_required
    def get(self, appointment_id=None):
        print(("GET appointment", appointment_id))
        if appointment_id:
            a = Appointment.query.get_or_404(appointment_id)
            print({
                "id": a.id,
                "doctor_id": a.doctor_id,
                "patient_id": a.patient_id,
                "date": a.slot.date.strftime("%Y-%m-%d"),
                "status": a.status.value,
                "bill": a.bill,
            })
            return {
                "id": a.id,
                "doctor_id": a.doctor_id,
                "patient_id": a.patient_id,
                "date": a.slot.date.strftime("%Y-%m-%d"),
                "status": a.status.value,
                "bill": a.bill,
            }, 200

        appts = Appointment.query.all()
        return [
            {
                "id": a.id,
                "doctor_id": a.doctor_id,
                "patient_id": a.patient_id,
                "date": a.slot.date.strftime("%Y-%m-%d"),
                "status": a.status.value,
                "bill": a.bill,
            } for a in appts
        ], 200

    @patient_required
    def post(self):
        data, error = get_json_data()
        if error: return error

        doctor_id = data.get("doctor_id")
        date_str = data.get("date")
        patient_id = current_user.id

        if not doctor_id or not date_str:
            return {"error": "doctor_id and date required"}, 400

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return {"error": "Invalid date format (YYYY-MM-DD required)"}, 400

        appt = Appointment(doctor_id=doctor_id, patient_id=patient_id, date=date, status="booked")
        db.session.add(appt)
        db.session.commit()
        return {"message": "Appointment booked", "id": appt.id}, 201


    @login_or_token_required
    def put(self, appointment_id):
        appt = Appointment.query.get_or_404(appointment_id)
        data, error = get_json_data()
        if error: return error

        status = data.get("status")
        if status not in ["booked", "completed", "cancelled"]:
            return {"error": "Invalid status"}, 400

        if status == "cancelled":
            appt.cancel()
        db.session.commit()
        return {"message": f"Appointment {status}"}, 200


    @admin_required
    def delete(self, appointment_id):
        appt = Appointment.query.get_or_404(appointment_id)
        db.session.delete(appt)
        db.session.commit()
        return {"message": "Appointment deleted"}, 200


# ----------------------------------------------------------------------------- #
class APILoginResource(Resource):
    def post(self):
        data, error = get_json_data()
        if error: return error

        email = data.get("email")
        password = data.get("password")
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if not user.api_token:
                user.generate_token()
                db.session.commit()
            return {"token": user.api_token, "user_id": user.id, "role": user.role}, 200

        return {"error": "Invalid credentials"}, 401
@api_bp.route("/billing_data")
@login_or_token_required
def billing_data():
    filter_type = request.args.get("type")
    filter_id = request.args.get("id")
    ap = get_appointment_rows(active=False)
    doctor_id,patient_id = None,None
    if current_user.role == "doctor":
        if filter_type == "department":
            ap = [a for a in ap if a["patient_id"] == int(filter_id) and a["doctor_id"] == current_user.id]
        
    elif current_user.role == "patient":
        if filter_type == "department":
            ap = [a for a in ap if a["department_id"] == int(filter_id) and a["patient_id"] == current_user.id]
        else:
            ap = [a for a in ap if a["patient_id"] == current_user.id and a["doctor_id"] == int(filter_id)]
    else:
        if filter_type == "department":
            ap = [a for a in ap if a["department_id"] == int(filter_id)]
        elif filter_type == "doctor":
            ap = [a for a in ap if a["doctor_id"] == int(filter_id)]
    # print(ap)
    
    results={}
    for a in ap:
        key = a["Date"]
        results[key] = results.get(key,0) + (a["Bill"] or 0)
    labels = sorted(results.keys())
    values = [results[k] for k in labels]
    # query = Appointment.query.join(Doctor)
    # doc_ids=[]
    # if filter_type == "department":
    #     dep = Department.query.get_or_404(filter_id)
    #     doc_ids = [doc.id for doc in dep.doctors]
    # elif filter_type == "doctor":
    #     doc_ids = [filter_id]

    # data = {}
    # for d in doc_ids:
    #     ap = get_appointment_rows(doc_id=d,active=False)
    #     for a in ap:
    #         key = a["Date"]
    #         data[key] = data.get(key, 0) + (a["Bill"] or 0) 

    # labels = sorted(data.keys())
    # values = [data[k] for k in labels]
    return {"labels": labels, "values": values}, 200

api.add_resource(DoctorResource,
                 "/doctors",
                 "/doctors/<int:doctor_id>")

api.add_resource(AppointmentResource,
                 "/appointments",
                 "/appointments/<int:appointment_id>")

api.add_resource(APILoginResource, "/login")