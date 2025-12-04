"""
Face recognition endpoints: registration (student uploads/captures face) and recognition (faculty sends live frame).
Store/retrieve embeddings/images from DB using simple OpenCV-based feature vectors.
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import numpy as np
import cv2

from models.face_model import register_face_embedding, get_all_faces
from models.student_model import get_student_by_id

face_bp = Blueprint("face", __name__, url_prefix="/face")

def extract_embedding(image_data: bytes):
    """
    Convert raw image bytes into a deterministic embedding using OpenCV.
    Steps:
      - Decode image bytes to grayscale
      - Resize to 32x32
      - Flatten + normalize (0-1) to create a 1024-length embedding
    """
    if not image_data:
        raise ValueError("No image data provided for embedding.")
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Unable to decode image.")
    img = cv2.resize(img, (32, 32))  # 32x32 -> 1024 dims
    emb = img.flatten().astype(np.float32) / 255.0
    return emb.tolist()

@face_bp.route("/register", methods=["POST"])
def register_face():
    """
    Student uploads/captures face for registration. Expects: student_id, image (base64 or file upload supported).
    Stores: embedding, student_id, image_url (path), created_at.
    """
    student_id = request.form.get('student_id') or (request.json or {}).get('student_id')
    file = request.files.get('image')
    if not (student_id and (file or request.data)):
        return jsonify({"error": "Missing student_id or image."}), 400
    image_bytes = file.read() if file else request.data
    try:
        embedding = extract_embedding(image_bytes)
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    image_url = f"https://fake-storage.example/{student_id}/{datetime.now().isoformat()}.jpg"  # Stub
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
    file = request.files.get('image')
    subject_id = request.form.get('subject_id') or (request.json or {}).get('subject_id')
    if not (file or request.data):
        return jsonify({"error": "Missing image data."}), 400
    try:
        query_embedding = extract_embedding(file.read() if file else request.data)
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    min_dist = float('inf')
    best = None
    for face in get_all_faces():
        db_emb = face.get('embedding')
        if not db_emb: continue
        if len(db_emb) != len(query_embedding):
            continue
        dist = float(np.linalg.norm(np.array(query_embedding) - np.array(db_emb)))
        if dist < min_dist:
            min_dist = dist
            best = face
    # Threshold tuned for normalized grayscale embeddings
    if best and min_dist < 5.0:
        # Found a match; get student info for marking
        student = get_student_by_id(best['student_id'])
        return jsonify({"student": student, "dist": round(min_dist, 4)})
    else:
        return jsonify({"error": "No matching student found."}), 404
