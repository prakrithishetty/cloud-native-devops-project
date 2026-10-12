
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from config import Config
from database import get_db_connection

app = Flask(__name__)
app.secret_key = "local-development-secret-change-me"


@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        version = request.form.get("version", "").strip()
        environment = request.form.get("environment", "").strip()

        if not version or environment not in ["Development", "Testing", "Production"]:
            flash("Enter a version and select a valid environment.", "error")
            return redirect(url_for("dashboard"))

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO deployments (version, environment, status) VALUES (%s, %s, %s) RETURNING id",
                (version, environment, "SUCCESS")
            )
            deployment_id = cursor.fetchone()[0]
            connection.commit()
            flash(
                f"Deployment record #{deployment_id} saved. This records a deployment; it does not deploy to a server.",
                "success"
            )
        except Exception:
            if connection:
                connection.rollback()
            app.logger.exception("Could not save deployment")
            flash("Could not save the deployment. Check the database.", "error")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return redirect(url_for("dashboard"))

    deployments = []
    database_status = "Connected"
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, version, environment, status, deployed_at FROM deployments ORDER BY deployed_at DESC, id DESC"
        )
        for row in cursor.fetchall():
            deployments.append({
                "id": row[0],
                "version": row[1],
                "environment": row[2],
                "status": row[3],
                "deployed_at": row[4].strftime("%Y-%m-%d %H:%M:%S") if row[4] else "N/A"
            })
    except Exception:
        database_status = "Disconnected"
        app.logger.exception("Could not load deployments")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return render_template(
        "dashboard.html",
        deployments=deployments,
        database_status=database_status
    )


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "version": Config.APP_VERSION,
        "service": "cloud-native-devops-app"
    })


@app.route("/api/status")
def api_status():
    return jsonify({
        "application": "running"
    })


@app.route("/api/info")
def info():
    return jsonify({
        "application": Config.APP_NAME,
        "version": Config.APP_VERSION,
        "environment": Config.ENVIRONMENT,
        "status": "running"
    })


@app.route("/api/users", methods=["GET", "POST"])
def api_users():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        if request.method == "POST":
            data = request.get_json(silent=True) or {}
            name = str(data.get("name", "")).strip()
            role = str(data.get("role", "")).strip()

            if not name or not role:
                return jsonify({"error": "name and role are required"}), 400

            cursor.execute(
                "INSERT INTO users (name, role) VALUES (%s, %s) RETURNING id, name, role",
                (name, role)
            )
            row = cursor.fetchone()
            connection.commit()
            return jsonify({"id": row[0], "name": row[1], "role": row[2]}), 201

        cursor.execute("SELECT id, name, role FROM users ORDER BY id")
        users = [
            {"id": row[0], "name": row[1], "role": row[2]}
            for row in cursor.fetchall()
        ]
        return jsonify(users)

    except Exception:
        if connection:
            connection.rollback()
        app.logger.exception("User API failed")
        return jsonify({"error": "User operation failed"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route("/api/deployments", methods=["GET", "POST"])
def api_deployments():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        if request.method == "POST":
            data = request.get_json(silent=True) or {}
            version = str(data.get("version", "")).strip()
            environment = str(data.get("environment", "")).strip()
            status = str(data.get("status", "SUCCESS")).strip()

            if not version or environment not in ["Development", "Testing", "Production"]:
                return jsonify({"error": "Valid version and environment are required"}), 400

            if status not in ["SUCCESS", "FAILED"]:
                return jsonify({"error": "status must be SUCCESS or FAILED"}), 400

            cursor.execute(
                "INSERT INTO deployments (version, environment, status) VALUES (%s, %s, %s) RETURNING id, version, environment, status",
                (version, environment, status)
            )
            row = cursor.fetchone()
            connection.commit()
            return jsonify({
                "id": row[0],
                "version": row[1],
                "environment": row[2],
                "status": row[3]
            }), 201

        cursor.execute(
            "SELECT id, version, environment, status, deployed_at FROM deployments ORDER BY deployed_at DESC, id DESC"
        )
        deployments = [{
            "id": row[0],
            "version": row[1],
            "environment": row[2],
            "status": row[3],
            "deployed_at": row[4].isoformat() if row[4] else None
        } for row in cursor.fetchall()]

        return jsonify(deployments)

    except Exception:
        if connection:
            connection.rollback()
        app.logger.exception("Deployment API failed")
        return jsonify({"error": "Deployment operation failed"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
