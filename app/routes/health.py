from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "application": "Cloud-Native DevOps Platform",
        "version": "1.0.0"
    })


@health_bp.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "application": "running",
        "environment": "development",
        "database": "not_connected",
        "docker": "not_configured",
        "cicd": "not_configured"
    })