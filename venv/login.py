from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Simple in-memory "database"
users_db = {
    # example:
    # "buyer@example.com": {"password": <hashed>, "role": "buyer"}
}

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")  # 'seller' or 'buyer'

    if not email or not password or role not in ["buyer", "seller"]:
        return jsonify({"error": "Invalid input"}), 400

    if email in users_db:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    users_db[email] = {"password": hashed_password, "role": role}

    return jsonify({"message": f"{role.capitalize()} registered successfully!"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    user = users_db.get(email)
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    role = user["role"]
    return jsonify({"message": f"Login successful as {role}!"}), 200


if __name__ == "__main__":
    app.run(debug=True)