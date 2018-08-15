#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2
import sys
import os

con = None

#con = psycopg2.connect(
   # "host='localhost' dbname='ride_my_way' user='postgres' password='namungoona'")
con = psycopg2.connect(
    "host='ec2-54-243-253-24.compute-1.amazonaws.com' dbname='d176ms9middb04' user='ycluqmdmwbcxrb' password='c9dee8fe6483f025b2096e72f39c8e1adc835f18635c4f519e14268e40143d33'")

create_users = """CREATE OR REPLACE FUNCTION public.create_users(
	usn character varying,
	em character varying,
	pass text,
	isd integer)
    RETURNS integer
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
AS $BODY$
declare
	total integer;

BEGIN
   INSERT INTO all_users (username,email,password_,isDriver,login_status)  VALUES(usn,
																			em,
											PGP_SYM_ENCRYPT(pass,'AES_KEY'),isd,'0');
   RETURN 1;
END;

$BODY$;

ALTER FUNCTION public.create_users(character varying, character varying, text, integer)
    OWNER TO postgres;

"""
