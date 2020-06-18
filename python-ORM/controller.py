from flask import Flask, request, jsonify
from flask_cors import CORS
from user import User
from util import create_session, lookup_pk_by_session

app = Flask(__name__)
CORS(app)

@app.route("/add_user", methods=["POST"])
def add_user():
    user_info = request.get_json()
    if user_info:
        if User.exists_user_with_email(user_info["email"]):
            return jsonify({"connected": True, "added": False})
        else:
            new_user = User(**user_info)
            new_user.save()
            return jsonify({"connected": True, "added": True})
    else:
        return jsonify({"connected": False})

@app.route("/login_user", methods=["POST"])
def login_user():
    user_info = request.get_json()
    if user_info:
        logged_in_user = User.login(user_info["email"], user_info["password"])
        if logged_in_user:
            token = create_session(logged_in_user.pk)
            return jsonify({"connected": True, "loggedIn": True, 
                             "token": token})
        else:
            return jsonify({"connected": True, "loggedIn": False})
    else:
        return jsonify({"connected": False})

@app.route("/create_diet", methods=["POST"])
def create_diet():
    success = True
    user_info = request.get_json()
    if user_info:
        pk = lookup_pk_by_session(user_info[token])
        current_user = User.user_for_pk(pk)
        #continue here

if __name__ == "__main__":
    app.run(debug=True)