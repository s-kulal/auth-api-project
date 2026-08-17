from flask import Flask, request, jsonify

app = Flask(__name__)

users = {
    "admin": "admin123",
    "subhash": "user123"
}

@app.route("/")
def home():
    return {"message":"Auth API Project"}

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if username in users and users[username] == password:
        token = username + '-token'

        return jsonify({
            "token": token
        }), 200

    return jsonify({
        "error": "Invalid Credentials"
    }), 401
    

if __name__ == "__main__":
    app.run(debug=True)



