from functools import wraps
import secrets

from flask import request, jsonify

from drone_inventory.models import Drone, User

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None #assume no one has access to the application .... we are verifying the token

        if 'x-access-token' in request.headers:
            #everytime we make a request on insomnia, it will have a header
            token = request.headers['x-access-token'].split(' ')[1] #place token inside of the 'x-access-token'. 
            #if its in request.headers, then grab the dictionary, the key = x-access-token, the value is a string. 
            #split the string on ' ' and get the back end of the value (Bearer db372...).
        if not token:
            return jsonify({"message": "Token is missing!"}), 401 #401 code
        
        #verify that a user has this token
        
        try:
            current_user_token = User.query.filter_by(token = token).first() #if the token is invalid or there is an error then it would go to the exception. 
            #scoping???

        except:
            owner = User.query.filter_by(token = token).first()
            if token !=  owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({"message": "Token is invalid"})
        
        return our_flask_function(current_user_token, *args, **kwargs)
    
    return decorated


import decimal
from flask import json

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert the decimal value into a string, decimal values are hard to serialize compare to string
            return str(obj)
        return super(JSONEncoder, self).default(obj)