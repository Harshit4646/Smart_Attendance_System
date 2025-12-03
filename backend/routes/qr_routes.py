"""
QR code attendance endpoints: generate and scan QR for attendance.
- /qr/generate/<student_id> : returns QR content (student id + token)
- /qr/scan : faculty sends scanned QR, backend decodes, verifies and marks attendance
"""
from flask import Blueprint, jsonify, request
#from ..models.student_model import get_student_by_id
from uuid import uuid4

qr_bp = Blueprint("qr", __name__, url_prefix="/qr")

@qr_bp.route("/generate/<student_id>", methods=["GET"])
def generate_qr(student_id):
    """
    Generates QR string for student, including a security token. (QR image generation TODO.)
    """
    # For real: use qrcode and return as image; here: provide raw data
    qr_token = str(uuid4())
    qr_data = {
        'student_id': student_id,
        'token': qr_token
    }
    qr_content = f"{student_id}:{qr_token}"
    return jsonify({"qr": qr_content, "data": qr_data})

@qr_bp.route("/scan", methods=["POST"])
def scan_qr():
    """
    Faculty uploads a scanned QR (raw: student_id + token). Backend verifies and marks attendance. (Token verification is a stub.)
    """
    data = request.json
    qr_content = data.get('qr_content')
    if not qr_content or ':' not in qr_content:
        return jsonify({"error": "Invalid or missing QR content."}), 400
    student_id, token = qr_content.split(':', 1)
    # TODO: verify against DB/session/person's token! (Not implemented)
    # For demo: just return success with student id
    return jsonify({"student_id": student_id, "status": "marked (demo)"})
