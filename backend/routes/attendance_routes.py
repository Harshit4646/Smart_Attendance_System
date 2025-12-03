"""
Attendance API endpoints: mark attendance, get today's attendance, etc.
"""
from flask import Blueprint, jsonify, request
from models.attendance_model import mark_attendance, get_attendance_by_student, get_attendance_by_date
from datetime import datetime, date

attendance_bp = Blueprint("attendance", __name__, url_prefix="/attendance")

@attendance_bp.route("/mark", methods=["POST"])
def mark():
    """
    General manual attendance marking by faculty/admin. Expects: student_id, subject_id, status (present/absent), optionally date/time.
    """
    data = request.json
    for field in ["student_id", "subject_id", "status"]:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    record = {
        **data,
        'attendance_date': data.get('attendance_date') or date.today().isoformat(),
        'attendance_time': data.get('attendance_time') or datetime.now().strftime('%H:%M:%S'),
    }
    saved = mark_attendance(record)
    return jsonify({"attendance": saved})

@attendance_bp.route("/mark-qr", methods=["POST"])
def mark_qr():
    """
    Mark attendance using QR scan. Expects: student_id, token. (Token verification not implemented here.)
    """
    data = request.json
    student_id = data.get("student_id")
    subject_id = data.get("subject_id")
    token = data.get("token")
    if not all([student_id, subject_id, token]):
        return jsonify({"error": "Missing student_id, subject_id, or token."}), 400
    # TODO: Validate token for student_id (not implemented; recommended for security)
    record = {
        'student_id': student_id,
        'subject_id': subject_id,
        'status': 'present',
        'attendance_date': date.today().isoformat(),
        'attendance_time': datetime.now().strftime('%H:%M:%S'),
    }
    saved = mark_attendance(record)
    return jsonify({"attendance": saved})

@attendance_bp.route("/mark-face", methods=["POST"])
def mark_face():
    """
    Mark attendance via face recognition.
    Expects: student_id (already recognized), subject_id.
    """
    data = request.json
    student_id = data.get("student_id")
    subject_id = data.get("subject_id")
    if not all([student_id, subject_id]):
        return jsonify({"error": "Missing student_id or subject_id."}), 400
    record = {
        'student_id': student_id,
        'subject_id': subject_id,
        'status': 'present',
        'attendance_date': date.today().isoformat(),
        'attendance_time': datetime.now().strftime('%H:%M:%S'),
    }
    saved = mark_attendance(record)
    return jsonify({"attendance": saved})

@attendance_bp.route("/today", methods=["GET"])
def get_today():
    """
    Return all attendance records for today (optionally, for a class/subject)
    """
    today = date.today().isoformat()
    all_today = get_attendance_by_date(today)
    return jsonify({"attendance": all_today})

