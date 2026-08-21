from flask import Flask, request, jsonify

app = Flask(__name__) # create Flask application 

users = {               # fake database, it is just python dictionary 
    "admin": {
        "password": "admin123",
        "role": "admin"
    },
    "subhash": {
        "password": "user123",
        "role": "user"
    }
}

tokens = {}

@app.route("/")     # Home endpoint -> decorator
def home(): # this runs when someone reaches "/"
    return {
        "message":"Auth API Project"
    } # client receives this message

# Login endpoint

@app.route("/login", methods=["POST"])    # login endpoint
# POST is used bcs we are sending users ={"admin" ...} to the server
def login(): # login function 
    data = request.get_json()  # read json 
    # now data contains user ={"username": "admin", ...}

    username = data.get("username")
    password = data.get("password")

    token = username + "-token"

    if username in users and users[username]["password"] == password: #authentication check
        tokens[token] = {
            "username": username,
            "role": users[username]["role"]
        }
    
        return jsonify({   # success response
            "username": tokens[token]["username"],
            "role": tokens[token]["role"]
        }), 200

    return jsonify({
        "error": "Invalid Credentials"
    }), 401


# Authenticate user    ->    Function definition 

def authenticate():
    auth_header = request.headers.get("Authorization") # gets "Bearer admin-token"
    
    if not auth_header:
        return None
    
    token = auth_header.replace("Bearer ", "") # replace "Bearer " with "" then 
                                               # extract token  -> admin-token
    return tokens.get(token)                                   
    # bcs the endpoint needs {"username": "admin", "role":"admin"}

# Profile endpoint

@app.route("/profile")
def profile():

    user = authenticate()

    if not user: # validate tokens
        return jsonify({
            "error": "Invalid Token"
        }), 401

    return jsonify({
        "username": user["username"]
    }), 200


# Create user endpoint

@app.route("/create-user", methods=["POST"])
def create_user():

    user = authenticate()

    if not user:         # Check token  -> from the authentication
        return jsonify({
            "error": "Invalid Token"
        }), 401

    if user["role"] != "admin": # aunthenticating the role 
        return jsonify({        # to decide the authorization
            "error": "Forbidden"# highest previlage is given to admin only 
        }), 403                 # or depends but usully admin 

    # to create new user
    data = request.get_json() # once they enter details fetched to data

    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    users[username] = {
        "password" : password,
        "role" : role
    }

    return jsonify({
        "message": "User Created Successfully"
    }), 201

# Launch FLASK
if __name__ == "__main__": # start server -> run this only if app.py is executed
    # app.run(debug=True) # launch flask 
    app.run(host="0.0.0.0", debug=True)
    # bcd 0.0.0.0 listens to all network interfaces


