from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, reqparse
import re
import json
import simplejson as json
from app.db_config import con
import psycopg2
import sys
from decimal import Decimal

def insert_ride_offers():
    """Getting data from the URL body """
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('details', type=str, required=True)
    parser.add_argument('price', type=str, required=True)
    #parser.add_argument('driver', type=str,required=True)
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
        if row is None:
             return make_response(jsonify({"message": "No ride offers found."}),
                                 404)
        results.append(dict(zip(columns, row)))
        
    print (str(results))
    return make_response(jsonify({"ride_offers": str(results),
                                          "status": "success"}),
                                 200)

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

