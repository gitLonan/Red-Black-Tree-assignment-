from flask_jwt_extended import create_access_token


from flask import request, jsonify



def init_JWT_auth(bp_jwt_auth):

    @bp_jwt_auth.route("/login", methods=["POST"])
    def login():
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        if username != "test" or password != "test":
            return jsonify({"msg": "Bad username or password"}), 401

        access_token = create_access_token(identity=username)
        
        return jsonify(access_token=access_token)


    
    

