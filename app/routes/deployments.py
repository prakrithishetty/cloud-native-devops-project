from flask import Blueprint, jsonify, request

deployments_bp = Blueprint("deployments", __name__)


deployments = [
    {
        "version": "v1.0.0",
        "status": "SUCCESS",
        "environment": "Development"
    },
    {
        "version": "v0.9.0",
        "status": "SUCCESS",
        "environment": "Development"
    }
]


@deployments_bp.route("/api/deployments", methods=["GET"])
def get_deployments():
    return jsonify(deployments)


@deployments_bp.route("/api/deployments", methods=["POST"])
def create_deployment():
    data = request.get_json()

    if not data or "version" not in data:
        return jsonify({
            "error": "version is required"
        }), 400

    deployment = {
        "version": data["version"],
        "status": data.get("status", "SUCCESS"),
        "environment": data.get(
            "environment",
            "Development"
        )
    }

    deployments.append(deployment)

    return jsonify(deployment), 201