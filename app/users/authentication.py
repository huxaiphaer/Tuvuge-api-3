from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, reqparse
import re
import json
import simplejson as json
from app.db_config import con
import psycopg2
import sys
from decimal import Decimal
import datetime
from werkzeug.security import generate_password_hash, \
    check_password_hash
import jwt
from datetime import datetime, timedelta
from flask import current_app


def create_user():
    """Getting data from the URL body """
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('email', type=str, required=True)
    parser.add_argument('password', type=str, required=True)
    args = parser.parse_args()

    username = args['username']
    email = args['email']
    password = args['password']

    if username.strip() == "" or len(username.strip()) < 2:
        return make_response(jsonify({"message":
                                      "invalid username, Enter correct username please"}),
                             400)

    if re.compile('[!@#$%^&*:;?><.0-9]').match(username):
        return make_response(jsonify({"message":
                                      "Invalid characters not allowed"}),
                             400)

    if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
        return make_response(jsonify({"message":
                                      "Enter valid email"}),
                             400)

    if password.strip() == "":
        return make_response(jsonify({"message":
                                      "Enter password"}),
                             400)
    if len(username) < 2:
        return make_response(jsonify({"message":
                                      "username  is too short, < 2"}),
                             400)

    if len(password) < 5:
        return make_response(jsonify({"message":
                                      "Password is too short, < 5"}),
                             400)

    """creating a sign up  cursor to check for already existing users."""
    cur = con.cursor()
    cur.callproc('check_if_user_exixts', (username,))
    row = cur.fetchone()
    while row is not None:
        status_value = str(row).strip().replace(
            '(', '').replace(')', '').replace(',', '')
        if int(status_value) == 0:
            print('go a head and insert data ')
            cur = con.cursor()
            isDriver = '0'
            cur.callproc('create_users', (username,
                                          email, password, isDriver,))
            con.commit()
            return make_response(jsonify({
                'message': 'user created successfully.',
                'status': 'success'},
            ), 201)
            break
        else:
            print('this username already exists.')
            return make_response(jsonify({"message":
                                          'Sorry,this username is already available.'}),
                                 400)
            break

# this method helps to login.


def login():
    """Getting data from the URL body """
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)
    args = parser.parse_args()
    # get username and password .
    username = args['username']
    password = args['password']

    cur = con.cursor()
    cur.callproc('login_auth', (username, password,))
    print(generate_password_hash(password))
    row = cur.fetchone()

    try:

        while row is not None:
            status_value = str(row).strip().replace(
                '(', '').replace(')', '').replace(',', '')
            if int(status_value) == 0:
                return make_response(jsonify({"message": "wrong credentials"}),
                                     401)
                break
            else:
                cur_get_username = con.cursor()
                cur_get_username.execute(
                    "select username from all_users where username ='"+username+"'")

                while True:
                    row = cur_get_username.fetchone()
                    print('--{}--'.format(row[0]))
                    access_token = "{}".format(generate_token(username))
                    return make_response(jsonify({"token": access_token,
                                                  "message": "User logged in successfully"
                                                  }), 200)
                    break

                break
    except TypeError as t:
        return make_response(jsonify({"message": "wrong credentials"}),
                             401)


def generate_token(username):
    """Generates the access token to be used as the Authorization header"""

    try:
        # set up a payload with an expiration time
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=30),
            # international atomic time
            'iat': datetime.utcnow(),
            # default  to user id
            'username': username
        }
        # create the byte string token using the payload and the SECRET key

        jwt_string = jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        ).decode('UTF-8')
        return jwt_string

    except Exception as e:
        # return an error in string format if an exception occurs
        return str(e)


def decode_token(token):
    """Decode the access token to get the payload 
    and return user_id and isDriver field results"""
    try:
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
        return {"username": payload['username'],
                "status": "Success"}
    except jwt.ExpiredSignatureError:
        return {"status": "Failure",
                "message": "Expired token. Please log in to get a new token"}
    except jwt.InvalidTokenError:
        return {"status": "Failure",
                "message": "Invalid token. Please register or login"}


class SignUp(Resource):
    def post(self):
        try:
            return create_user()

        except psycopg2.DatabaseError as e:
            if con:
                con.rollback()
                print(e)
                create_user()

            sys.exit(1)
        except psycopg2.InterfaceError as Ie:
            print(Ie)
            return create_user()


class SignIn(Resource):
    def post(self):
        try:
            return login()
        except psycopg2.DatabaseError as e:
            if con:
                con.rollback()
                login()
            sys.exit(1)
        except psycopg2.InterfaceError as Ie:
            print(Ie)
            return login()
