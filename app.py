from flask import Flask, request, jsonify

app = Flask(__name__) # create Flask application 

users = {               # fake database, it is just python dictionary 
    "admin": "admin123",
    "subhash": "user123"
}

tokens = {}

@app.route("/")     # Home endpoint -> decorator
def home(): # this runs when someone reaches "/"
    return {
        "message":"Auth API Project"
    } # client receives this message

@app.route("/login", methods=["POST"])    # login endpoint
# POST is used bcs we are sending users ={"admin" ...} to the server
def login(): # login function 
    data = request.get_json()  # read json 
    # now dats contains user ={"username": "admin", ...}

    username = data.get("username")
    password = data.get("password")

    if username in users and users[username] == password: #authentication check
        token = username + '-token'

        tokens[token] = username  # stored inside the tokens = {}

        return jsonify({   # success response
            "token": token
        }), 200

    return jsonify({
        "error": "Invalid Credentials"
    }), 401

@app.route("/profile")
def profile():

    auth_header = request.headers.get("Authorization") # gets "Bearer admin-token"

    if not auth_header:
        return jsonify({
            "error": "Token Missing"
        }), 401

    token = auth_header.replace("Bearer ", "") # replace "Bearer " with "" then 
                                               # extract token  -> admin-token

    if token not in tokens: # validate tokens
        return jsonify({
            "error": "Invalid Token"
        }), 401

    return jsonify({
        "username": tokens[token]
    }), 200
    

if __name__ == "__main__": # start server -> run this only if app.py is executed
    app.run(debug=True) # launch flask 



