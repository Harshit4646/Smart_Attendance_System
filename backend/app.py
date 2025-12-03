# app.py - Flask entry. Now enables all API blueprints for full system.
from flask import Flask, jsonify
from flask_cors import CORS
from .config import FLASK_SECRET_KEY
from .supabase_client import supabase
from .routes.auth_routes import auth_bp
from .routes.student_routes import student_bp
from .routes.faculty_routes import faculty_bp
from .routes.admin_routes import admin_bp
from .routes.attendance_routes import attendance_bp
from .routes.face_routes import face_bp
from .routes.qr_routes import qr_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = FLASK_SECRET_KEY
    CORS(app)

    # Register API blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(face_bp)
    app.register_blueprint(qr_bp)

    @app.route("/")
    def index():
        return jsonify({"message": "Attendance Backend Running"})

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
