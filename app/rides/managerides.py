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
from app.users.authentication import decode_token


class GetRides(Resource):

    def insert_ride_offers(self):
        """Getting data from the URL body """
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('details', type=str, required=True)
        parser.add_argument('price', type=str, required=True)
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        """ check the token value if its available"""
        if not args['token']:
            return make_response(jsonify({"message":
                                          "Token is missing"}),
                                 401)
        """ implementing token decoding"""
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message":
                                          decoded["message"]}),
                                 401)

        offer_name = args['name']
        offer_details = args['details']
        price = args['price']
        """creating a ride offer cursor to check for already existing ride offer names."""
        cur_select_ride_offers = con.cursor()
        cur_select_ride_offers.execute(
            "select name from rides where driver = 'Huza' and name='"+offer_name+"'")
        while True:
            row = cur_select_ride_offers.fetchone()
            if row == None:
                break

            if str(row[0]).strip() == str(offer_name).strip():
                print('db name : ' + str(row[0]) +
                      '  url name : ' + str(offer_name).strip())
                return make_response(jsonify({"message":
                                              'Sorry,this ride offer is already available.'}),
                                     400)

        cur = con.cursor()
        cur.execute("INSERT INTO rides (name,details,price,driver)  VALUES('" +
                    offer_name + "','"+offer_details+"','"+price+"','Huza')")
        con.commit()
        return make_response(jsonify({
            'message': 'Ride offer created successfully.'},
        ), 201)

    def get_ride_offers(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message":
                                          "Token is missing"}),
                                 401)
        """ implementing token decoding"""
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message":
                                          decoded["message"]}),
                                 401)

        cur = con.cursor()
        cur.execute(
            """select id, name,details,driver, price  from rides""")
        columns = ('id', 'name', 'details',
                   'driver', 'price'
                   )
        results = []
        for row in cur.fetchall():
            if row is None:
                return make_response(jsonify({"message": "No ride offers found."}),
                                     404)
            results.append(dict(zip(columns, row)))

        print(str(results))
        return make_response(jsonify({"ride_offers": str(results)}),
                             200)

    def post(self):

        try:

            return self.insert_ride_offers()

        except psycopg2.DatabaseError as e:
            if con:
                con.rollback()
                print(e)
                self.insert_ride_offers()

            sys.exit(1)
        except psycopg2.InterfaceError as Ie:
            print(Ie)
            return self.insert_ride_offers()

    def get(self):
        try:
            return self.get_ride_offers()
        except psycopg2.DatabaseError as e:
            if con:
                print(e)
                con.rollback()
                return self.get_ride_offers()
        except psycopg2.InterfaceError as Ie:
            print(Ie)
            return self.get_ride_offers()


class GetSingleRide(Resource):
    def get_single_ride(self, ride_id):
        """Getting data from the URL body """
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message":
                                          "Token is missing"}),
                                 401)
        """ implementing token decoding"""
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message":
                                          decoded["message"]}),
                                 401)
        cur = con.cursor()
        cur.execute(
            "select id , name , details , driver, price from rides  where id='"+ride_id+"' ")
        columns = ('id', 'name', 'details',
                   'driver', 'price')
        results = []

        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))
            if row is not None:
                return make_response(jsonify({
                    "ride_offer": str(results).replace("[", "").replace("]", "")
                }), 200)

        return make_response(jsonify({"message":
                                      "sorry please , ride offer not found, try searching again"}),
                             404)

    def get(self, ride_id):
        try:
            return self.get_single_ride(ride_id)
        except psycopg2.DatabaseError as e:
            if con:
                print(e)
                con.rollback()
                return self.get_single_ride(ride_id)
        except psycopg2.InterfaceError as Ie:
            print(Ie)
            return self.get_single_ride(ride_id)


class CreateRideRequests(Resource):
    def create_rideoffer_reuests(self, rideoffer_id):
        """check whether ride offers exist."""
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message":
                                          "Token is missing"}),
                                 401)
        """ implementing token decoding"""
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message":
                                          decoded["message"]}),
                                 401)

        check_ride_offer_cur = con.cursor()
        check_ride_offer_cur.execute(
            "select id from rides where id='"+rideoffer_id+"'")
        while True:
            row = check_ride_offer_cur.fetchone()
            if row is None:
                print(row)
                return make_response(jsonify({"message":
                                              "sorry please , ride offer not found"}), 404)
                # break
            else:

                cur_select_ride_offers = con.cursor()
                """checking whether the ride request for the user already exists."""
                cur_select_ride_offers.execute(
                    "select ride_offer_id from requests where passengername = 'Huza' and ride_offer_id='"+rideoffer_id+"'")
                while True:
                    row = cur_select_ride_offers.fetchone()
                    if row == None:
                        break

                    if str(row[0]).strip() == str(rideoffer_id).strip():
                        print('db name : ' + str(row[0]) +
                              '  url name : ' + str(rideoffer_id).strip())
                        return make_response(jsonify({"message":
                                                      'Sorry,you have  already made a ride request.'}),
                                             400)

            cur = con.cursor()

            formated_time_date = datetime.datetime.now()
            formated_time_date.strftime('%H-%M-%Y-%m-%d')
            cur.execute("INSERT INTO requests (passengername,time,ride_offer_id,status)  VALUES('Huza','" +
                        str(formated_time_date)+"','"+rideoffer_id+"','0')")
            con.commit()
            return make_response(jsonify({
                'message': 'Ride request created successfully.'},
            ), 201)

    def post(self, rideoffer_id):
        try:
            return self.create_rideoffer_reuests(rideoffer_id)

        except psycopg2.DatabaseError as e:
            if con:
                con.rollback()
                print(e)
                self.create_rideoffer_reuests(rideoffer_id)

            sys.exit(1)
        except psycopg2.InterfaceError as Ie:
            print(Ie)
            return self.create_rideoffer_reuests(rideoffer_id)


class GetRideOfferRequests(Resource):

    def get_rideoffer_requests(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message":
                                          "Token is missing"}),
                                 401)
        """ implementing token decoding"""
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message":
                                          decoded["message"]}),
                                 401)

        cur = con.cursor()
        cur.execute(
            "select id, passengername,time  from requests where ride_offer_id= '"+id+"'")
        columns = ('id', 'passengername', 'time'
                   )
        results = []
        for row in cur.fetchall():
            if row is not None:
                results.append(dict(zip(columns, row)))
                print(str(results))
                return make_response(jsonify({"ride_offers": str(results).replace('[', '').replace(']', '')}),
                                     200)
        return make_response(jsonify({"message": "No ride requests found."}),
                             404)

    def get(self, rideId):
        try:
            return self.get_rideoffer_requests(rideId)

        except psycopg2.DatabaseError as e:
            if con:
                con.rollback()
                print(e)
                self.get_rideoffer_requests(rideId)

            sys.exit(1)
        except psycopg2.InterfaceError as Ie:
            print(Ie)
            return self.get_rideoffer_requests(rideId)


class AcceptOrRejectOffer(Resource):

    def accept_or_reject_ridrequest(self, rideId, requestId):

        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, required=True)
        parser.add_argument('token', location='headers')
        args = parser.parse_args()

        if not args['token']:
            return make_response(jsonify({"message":
                                          "Token is missing"}),
                                 401)
        """ implementing token decoding"""
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message":
                                          decoded["message"]}),
                                 401)

        status = args['status']

        cur = con.cursor()
        cur.execute(
            "select id from requests where ride_offer_id= '"+rideId+"' and id ='"+requestId+"' ")
        for row in cur.fetchall():
            if row is not None:

                if int(status) == 0:
                    cur = con.cursor()
                    cur.execute(
                        "update  requests SET status  ='"+status+"' where ride_offer_id = '"+rideId+"' "
                    )
                    return make_response(
                        jsonify({"message": "ride request  rejected"}), 200
                    )

                else:
                    cur = con.cursor()
                    cur.execute(
                        "update  requests SET status  ='"+status+"' where ride_offer_id = '"+rideId+"' ")
                    return make_response(
                        jsonify({"message": "ride request  accepted"}), 200
                    )
            return make_response(
                jsonify({"message": "ride offer is not found please "}), 404
            )

    def put(self, rideId, requestId):
        try:
            return self.accept_or_reject_ridrequest(rideId, requestId)
        except psycopg2.DatabaseError as e:
            if con:
                con.rollback()
                print(e)
                self.accept_or_reject_ridrequest(rideId, requestId)

            sys.exit(1)
        except psycopg2.InterfaceError as Ie:
            print(Ie)
            return self.accept_or_reject_ridrequest(rideId, requestId)
