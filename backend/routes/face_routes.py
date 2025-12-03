"""
Face recognition endpoints: registration (student uploads/captures face) and recognition (faculty sends live frame). Store/retrieve embeddings/images from DB. Actual face recognition logic is stubbed.
"""
from flask import Blueprint, request, jsonify
from models.face_model import register_face_embedding, get_all_faces, get_face_by_student_id
from models.student_model import get_student_by_id
from datetime import datetime
# Placeholder: Actual embedding extraction not implemented
import numpy as np

face_bp = Blueprint("face", __name__, url_prefix="/face")

def extract_embedding(image_data):
    """
    (Stub) Given an image, returns a fake embedding (128-dim list). Replace with actual model logic.
    """
    # TODO: Integrate DeepFace/face_recognition (real) in production
    return np.random.rand(128).tolist()

@face_bp.route("/register", methods=["POST"])
def register_face():
    """
    Student uploads/captures face for registration. Expects: student_id, image (base64 or file upload supported).
    Stores: embedding, student_id, image_url (path), created_at.
    """
    student_id = request.form.get('student_id') or (request.json or {}).get('student_id')
    # Accept file upload (multipart) or base64 (JSON); we simulate image storage as a URL
    file = request.files.get('image')
    image_url = f"https://fake-storage.example/{student_id}/{datetime.now().isoformat()}.jpg"  # Stub
    if not (student_id and (file or request.data)):
        return jsonify({"error": "Missing student_id or image."}), 400
    embedding = extract_embedding(file.read() if file else request.data)
    payload = {
        'student_id': student_id,
        'embedding': embedding,
        'image_url': image_url,
        'created_at': datetime.now().isoformat()
    }
    saved = register_face_embedding(payload)
    return jsonify({"face": saved})

@face_bp.route("/recognize", methods=["POST"])
def recognize_face():
    """
    Faculty scans webcam/image, backend returns closest student (auto-mark). Expects: image (base64/file), subject_id.
    """
    # Accept image as file or data; emulate match from DB
    file = request.files.get('image')
    subject_id = request.form.get('subject_id') or (request.json or {}).get('subject_id')
    # Simulate embedding extraction
    query_embedding = extract_embedding(file.read() if file else request.data)
    min_dist = float('inf')
    best = None
    for face in get_all_faces():
        db_emb = face.get('embedding')
        if not db_emb: continue
        # Simulate Euclidean distance (instead of face_recognition.compare_faces)
        dist = float(np.linalg.norm(np.array(query_embedding) - np.array(db_emb)))
        if dist < min_dist:
            min_dist = dist
            best = face
    if best and min_dist < 0.6:
        # Found a match; get student info for marking
        student = get_student_by_id(best['student_id'])
        return jsonify({"student": student, "dist": min_dist})
    else:
        return jsonify({"error": "No matching student found."}), 404

