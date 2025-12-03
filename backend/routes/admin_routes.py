"""
Routes for admin module: CRUD for all tables, analytics access.
"""
from flask import Blueprint, jsonify, request
from ..models.student_model import create_student, get_all_students, get_student_by_id, update_student, delete_student
from ..models.faculty_model import create_faculty, get_all_faculty, get_faculty_by_id, update_faculty, delete_faculty
from ..models.class_model import create_class, get_all_classes, get_class_by_id, update_class, delete_class
from ..models.subject_model import create_subject, get_all_subjects, get_subject_by_id, update_subject, delete_subject
from ..models.attendance_model import get_attendance_by_student

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ---------- Students ----------
@admin_bp.route("/students", methods=["GET", "POST"])
def students():
    if request.method == 'GET':
        return jsonify({"students": get_all_students()})
    elif request.method == 'POST':
        data = request.json
        created = create_student(data)
        return jsonify({"student": created}), 201

@admin_bp.route("/students/<student_id>", methods=["GET", "PUT", "DELETE"])
def manage_student(student_id):
    if request.method == 'GET':
        student = get_student_by_id(student_id)
        return jsonify({"student": student})
    elif request.method == 'PUT':
        updates = request.json
        updated = update_student(student_id, updates)
        return jsonify({"student": updated})
    elif request.method == 'DELETE':
        deleted = delete_student(student_id)
        return jsonify({"deleted": deleted})

# ---------- Faculty ----------
@admin_bp.route("/faculty", methods=["GET", "POST"])
def faculty():
    if request.method == 'GET':
        return jsonify({"faculty": get_all_faculty()})
    elif request.method == 'POST':
        data = request.json
        created = create_faculty(data)
        return jsonify({"faculty": created}), 201

@admin_bp.route("/faculty/<faculty_id>", methods=["GET", "PUT", "DELETE"])
def manage_faculty(faculty_id):
    if request.method == 'GET':
        faculty = get_faculty_by_id(faculty_id)
        return jsonify({"faculty": faculty})
    elif request.method == 'PUT':
        updates = request.json
        updated = update_faculty(faculty_id, updates)
        return jsonify({"faculty": updated})
    elif request.method == 'DELETE':
        deleted = delete_faculty(faculty_id)
        return jsonify({"deleted": deleted})

# ---------- Classes ----------
@admin_bp.route("/classes", methods=["GET", "POST"])
def classes():
    if request.method == 'GET':
        return jsonify({"classes": get_all_classes()})
    elif request.method == 'POST':
        data = request.json
        created = create_class(data)
        return jsonify({"class": created}), 201

@admin_bp.route("/classes/<class_id>", methods=["GET", "PUT", "DELETE"])
def manage_class(class_id):
    if request.method == 'GET':
        c = get_class_by_id(class_id)
        return jsonify({"class": c})
    elif request.method == 'PUT':
        updates = request.json
        updated = update_class(class_id, updates)
        return jsonify({"class": updated})
    elif request.method == 'DELETE':
        deleted = delete_class(class_id)
        return jsonify({"deleted": deleted})

# ---------- Subjects ----------
@admin_bp.route("/subjects", methods=["GET", "POST"])
def subjects():
    if request.method == 'GET':
        return jsonify({"subjects": get_all_subjects()})
    elif request.method == 'POST':
        data = request.json
        created = create_subject(data)
        return jsonify({"subject": created}), 201

@admin_bp.route("/subjects/<subject_id>", methods=["GET", "PUT", "DELETE"])
def manage_subject(subject_id):
    if request.method == 'GET':
        subj = get_subject_by_id(subject_id)
        return jsonify({"subject": subj})
    elif request.method == 'PUT':
        updates = request.json
        updated = update_subject(subject_id, updates)
        return jsonify({"subject": updated})
    elif request.method == 'DELETE':
        deleted = delete_subject(subject_id)
        return jsonify({"deleted": deleted})

# ---------- Analytics ----------
@admin_bp.route("/analytics", methods=["GET"])
def analytics():
    # Placeholder analytics summary for now.
    students = get_all_students() or []
    data = {
        "total_students": len(students),
        "avg_attendance": 87,  # TODO: Compute real average
        "at_risk_count": sum(1 for s in students if 0),  # Stub
    }
    return jsonify({"analytics": data})
