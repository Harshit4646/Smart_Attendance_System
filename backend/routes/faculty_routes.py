"""
Routes for faculty: view their classes and attendance.
"""
from flask import Blueprint, jsonify, request
from models.faculty_model import get_faculty_by_email
from models.class_model import get_all_classes
from models.attendance_model import get_attendance_by_class

faculty_bp = Blueprint("faculty", __name__, url_prefix="/faculty")

def get_email_from_request():
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        # TODO: decode JWT for email
        pass
    if 'email' in request.args:
        return request.args['email']
    elif 'email' in request.json or {}:
        return request.json.get('email')
    return None

@faculty_bp.route("/classes", methods=["GET"])
def get_classes():
    """
    Return list of classes taught by this faculty.
    """
    email = get_email_from_request()
    if not email:
        return jsonify({"error": "Missing faculty email."}), 401
    faculty = get_faculty_by_email(email)
    if not faculty:
        return jsonify({"error": "No faculty found."}), 404
    faculty_id = faculty['id']
    all_classes = get_all_classes()
    # Filter: classes where faculty_id == class['faculty_id'] (simulate join)
    classes = [c for c in all_classes if c.get('faculty_id') == faculty_id]
    return jsonify({"classes": classes})

@faculty_bp.route("/attendance/<class_id>", methods=["GET"])
def class_attendance(class_id):
    """
    Return all attendance records for the class (optionally, by date).
    """
    date = request.args.get("date")
    attendance = get_attendance_by_class(class_id)
    # In get_attendance_by_class(), you may further filter by date/subject on frontend.
    if date:
        attendance = [a for a in attendance if a['attendance_date'] == date]
    return jsonify({"attendance": attendance})

