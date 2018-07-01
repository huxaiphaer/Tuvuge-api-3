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

def insert_ride_offers():
    """Getting data from the URL body """
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('details', type=str, required=True)
    parser.add_argument('price', type=str, required=True)
    parser.add_argument('token', location='headers')
    args = parser.parse_args()

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
        'message': 'Ride offer created successfully.',
        'status': 'success'},
    ), 201)


def get_ride_offers():

    cur = con.cursor()
    cur.execute(
    """select id, name,details,driver, price  from rides""")
    columns = ('id', 'name', 'details',
     'driver','price'
     )
    results = []
    for row in cur.fetchall():
        if row is  None:
             return make_response(jsonify({"message": "No ride offers found."}),
                                 404)
        results.append(dict(zip(columns, row)))
        
    print (str(results))
    return make_response(jsonify({"ride_offers": str(results),
                                          "status": "success"}),
                                 200)


def get_single_ride(ride_id):
    cur = con.cursor()
    cur.execute("select id , name , details , driver, price from rides  where id='"+ride_id+"' ")
    columns = ('id','name','details',
    'driver','price')
    results = []

    for row in cur.fetchall():
        results.append(dict(zip(columns,row)))
        if row is not None :
             return make_response(jsonify({
        "ride_offer":str(results).replace("[","").replace("]",""),
        "status":"success"
    }),200)
            
         
    return make_response(jsonify({"message":
                                      "sorry please , ride offer not found, try searching again"}),
                             404)


def create_rideoffer_reuests(rideoffer_id):

    """check whether ride offers exist."""
    check_ride_offer_cur = con.cursor()
    check_ride_offer_cur.execute("select id from rides where id='"+rideoffer_id+"'")
    while True:
        row = check_ride_offer_cur.fetchone()
        if row is None:
             print(row)
             return make_response(jsonify({"message":
                                      "sorry please , ride offer not found"}),
                             404)
             break
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

            cur.execute("INSERT INTO requests (passengername,time,ride_offer_id,status)  VALUES('Huza','"+str(datetime.datetime.now())+"','"+rideoffer_id+"','0')")
            con.commit()
            return make_response(jsonify({
                'message': 'Ride request created successfully.',
                'status': 'success'},
            ), 201)


    

class GetRides(Resource):

    def post(self):

        try:
           
            return insert_ride_offers()

        except psycopg2.DatabaseError as e:
            if con:
                con.rollback()
                print(e)
                insert_ride_offers()

            sys.exit(1)
        except psycopg2.InterfaceError as Ie:
            print(Ie)
            return insert_ride_offers()

    def get(self):
        try:
            return get_ride_offers()
        except psycopg2.DatabaseError as e:
            if con:
                print(e)
                con.rollback()
                return get_ride_offers()
        except psycopg2.InterfaceError as Ie:
            print(Ie)
            return get_ride_offers()


class GetSingleRide(Resource):

    def get(self, ride_id):
        try:
            return get_single_ride(ride_id)
        except psycopg2.DatabaseError as e:
            if con:
                print(e)
                con.rollback()
                return get_single_ride(ride_id)
        except psycopg2.InterfaceError as Ie:
            print(Ie)
            return get_single_ride(ride_id)


class CreateRideRequests(Resource):
    def post(self, rideoffer_id):
        try:
            return create_rideoffer_reuests(rideoffer_id)

        except psycopg2.DatabaseError as e:
            if con:
                con.rollback()
                print(e)
                create_rideoffer_reuests(rideoffer_id)

            sys.exit(1)
        except psycopg2.InterfaceError as Ie:
            print(Ie)
            return create_rideoffer_reuests(rideoffer_id)
    

