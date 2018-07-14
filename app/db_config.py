#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2
import sys
import os

# DATABASE_URL = os.environ['postgres://yffaefhpyvbwkl:51460cce946c9ee2a98c6ef8e71e7e193b7e14bb3d0f8c26d8fe02bf5eb91dd6@ec2-54-83-203-198.compute-1.amazonaws.com:5432/d3fibeu3klt9e7']
con = None

#con = psycopg2.connect(
   # "host='localhost' dbname='ride_my_way' user='postgres' password='namungoona'")
con = psycopg2.connect(
    "host='ec2-54-243-253-24.compute-1.amazonaws.com' dbname='d176ms9middb04' user='ycluqmdmwbcxrb' password='c9dee8fe6483f025b2096e72f39c8e1adc835f18635c4f519e14268e40143d33'")
# con = psycopg2.connect(
#   "host='ec2-54-83-203-198.compute-1.amazonaws.com' dbname='d3fibeu3klt9e7' user='yffaefhpyvbwkl' password='51460cce946c9ee2a98c6ef8e71e7e193b7e14bb3d0f8c26d8fe02bf5eb91dd6'")#
