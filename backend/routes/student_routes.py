"""
Routes for student self-service: viewing info and attendance.
"""
from flask import Blueprint, jsonify, request
from models.student_model import get_student_by_email
from models.attendance_model import get_attendance_by_student

student_bp = Blueprint("student", __name__, url_prefix="/students")

def get_email_from_request():
    # In production, parse JWT token to get email; here, fallback to email query param for demo
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        # TODO: decode JWT (not implemented, needs secret)
        pass
    if 'email' in request.args:
        return request.args['email']
    elif 'email' in request.json or {}:
        return request.json.get('email')
    return None

@student_bp.route("/me", methods=["GET"])
def get_me():
    """
    Return student profile (from email in token or query param)
    """
    email = get_email_from_request()
    if not email:
        return jsonify({"error": "Missing email (should extract from token)"}), 401
    profile = get_student_by_email(email)
    if not profile:
        return jsonify({"error": "No student with this email."}), 404
    return jsonify({"student": profile})

@student_bp.route("/attendance", methods=["GET"])
def get_attendance():
    """
    Return attendance records for authenticated student.
    """
    email = get_email_from_request()
    if not email:
        return jsonify({"error": "Missing email (should extract from token)"}), 401
    profile = get_student_by_email(email)
    if not profile:
        return jsonify({"error": "No student with this email."}), 404
    student_id = profile['id']
    attendance = get_attendance_by_student(student_id)
    return jsonify({"attendance": attendance})

