"""
Handles Authentication endpoints for students, faculty, and admin using Supabase Auth.
/POST /auth/login: Expects email, password, role. Authenticates via Supabase, verifies role.
/POST /auth/logout: Placeholder; client should clear tokens/sessions
"""
from flask import Blueprint, request, jsonify
from supabase_client import supabase
from models.student_model import get_student_by_email
from models.faculty_model import get_faculty_by_email
#from ..models.admin_model import get_admin_by_email  # (If admin table is added)
from config import FLASK_SECRET_KEY

import os

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

ADMIN_EMAILS = os.getenv("ADMIN_EMAILS", "admin@example.com").split(",")

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login using Supabase Auth. Expects JSON: { email, password, role }
    Role is one of: student, faculty, admin. Returns: { token, user, role }, or error.
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not all([email, password, role]):
        return jsonify({"error": "Missing credentials."}), 400
    if role not in ["student", "faculty", "admin"]:
        return jsonify({"error": "Invalid role."}), 400

    # Supabase Auth sign-in
    auth_resp = supabase.auth.sign_in_with_password({"email": email, "password": password})
    session = getattr(auth_resp, 'session', None)
    user = getattr(auth_resp, 'user', None)
    if not session:
        return jsonify({"error": "Invalid email or password."}), 401

    # Role check by DB lookup
    if role == "student":
        profile = get_student_by_email(email)
        if not profile:
            return jsonify({"error": "No 'student' user with this email."}), 403
    elif role == "faculty":
        profile = get_faculty_by_email(email)
        if not profile:
            return jsonify({"error": "No 'faculty' user with this email."}), 403
    elif role == "admin":
        if email not in ADMIN_EMAILS:
            return jsonify({"error": "Not an admin email."}), 403
        profile = {"email": email, "role": "admin"}  # Optionally more fields

    # On success, return essential user profile, role, and access_token for frontend
    return jsonify({
        "token": session.access_token,
        "user": profile,
        "role": role
    })

@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    For stateless/sessionless setup: client should clear their token. For session-based backend,
    implement token blacklisting (not present here).
    """
    return jsonify({"message": "Logged out (token removed on client)."}), 200

