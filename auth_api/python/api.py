from flask import Flask
from flask import jsonify
from flask import request
from methods import Token, Restricted, Authorization

# APP CONFIGURATION
# -----------------

app = Flask(__name__)
# JWT encryption secret
secret = "my2w7wjd7yXF64FIADfJxNs1oupTGAuW"
# Classes to code
login = Token(secret)
protected = Restricted(secret)

# ENDPOINTS
# ---------

# Just a health check


@app.route("/")
def url_root():
    return "OK"


# Login endpoint - e.g. http://127.0.0.1:8000/login
@app.route("/login", methods=['POST'])
def url_login():
    # Get user data from request
    username = request.args.get('username')
    password = request.args.get('password')

    # Generate token using login Object
    token = login.generate_token(username, password)

    # Check if token is valid (it will be null if credentials are invalid)
    if token is not None:
        return token
    else:
        # If token is null (invalid credentials), return a 403 HTTP error message
        return '', 403


# Protected endpoint - e.g. http://127.0.0.1:8000/protected
@app.route("/protected")
def url_protected():
    # Get token from Authorization header
    data = request.headers.get('Authorization')
    auth_token = str.replace(str(data), "Bearer ", "")
    # Verify JWT token
    res = {
        "data": protected.access_data(auth_token)
    }
    return jsonify(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
