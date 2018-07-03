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

def create_user():
    """Getting data from the URL body """
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('email', type=str, required=True)
    parser.add_argument('password', type=str, required=True)
    parser.add_argument('isDriver', location='headers')
    args = parser.parse_args()

    username = args['username']
    email = args['email']
    password = args['password']
    isDriver = args['isDriver']

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

    if len(password) < 5:
        return make_response(jsonify({"message":
                                        "Password is too short, < 5"}),
                                400)


    """creating a sign up  cursor to check for already existing users."""
    cur = con.cursor()
    cur.execute(
        "select username from rides where username = '"+username+"'")
    while True:
        row = cur.fetchone()
        if row == None:
            break

        if str(row[0]).strip() == str(username).strip():
            print('db name : ' + str(row[0]) +
                  '  url name : ' + str(username).strip())
            return make_response(jsonify({"message":
                                          'Sorry,this username is already available.'}),
                                 400)

    cur = con.cursor()
    cur.execute("INSERT INTO users (username,email,password_,isDriver,login_status)  VALUES('" +
                username + "','"+email+"','"+password+"','"+isDriver+"','0')")
    con.commit()
    return make_response(jsonify({
        'message': 'user created successfully.',
        'status': 'success'},
    ), 201)



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
        