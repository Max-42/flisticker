# Authentication decorator
import datetime
from functools import wraps
from flask import app, flash, jsonify, make_response, redirect, request, url_for
import jwt
import os

import pytz

def is_admin(token: jwt) -> bool:
    try:
        decoded = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=['HS256'])
        # return decoded
        if decoded["admin"] == True:
            # check if the token is not older than 1 hour
            if (datetime.datetime.now(pytz.timezone('Europe/Berlin')) - datetime.datetime.fromtimestamp(decoded["iat"], pytz.timezone('Europe/Berlin'))).seconds < 3600:
                return True
            else:
                print("Login fehlgeschlagen: Token abgelaufen!")
                return False
        else:
            return False
    except jwt.ExpiredSignatureError:
        print("Login fehlgeschlagen: Token signatur abgelaufen!")
        return False
    except jwt.InvalidTokenError:
        print("Login fehlgeschlagen: Token ungültig!")
        return False


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
#        SECRET_KEY = 

        #get the cookie "KevTok" from the request
        if 'KevTok' in request.cookies:
            token = request.cookies['KevTok']
            if is_admin(token):
                return f(*args, **kwargs)
            else:
                flash("Deine Anmeldung ist ungültig oder abgelaufen!", "info")
                #redirect to login with a 401 status code
                return redirect(url_for('login'),code=401)
        else:
            flash("Token is missing!")
            return redirect(url_for('login'),code=401)

        #if token != "123": # check if token is "123"
        #    flash("Invalid token!")
        #    return make_response(jsonify({"message": "Invalid token!"}), 401)
        ## Return the user information attached to the token
        #return f(*args, **kwargs)
    return decorator