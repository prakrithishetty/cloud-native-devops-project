from flask import Blueprint, jsonify, request

users_bp = Blueprint("users", __name__)


users = [
    {
        "id": 1,
        "name": "Admin",
        "role": "DevOps Engineer"
    },
    {
        "id": 2,
        "name": "Developer",
        "role": "Developer"
    }
]


@users_bp.route("/api/users", methods=["GET"])
def get_users():
    return jsonify(users)


@users_bp.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({
            "error": "name is required"
        }), 400

    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "role": data.get("role", "Developer")
    }

    users.append(new_user)

    return jsonify(new_user), 201