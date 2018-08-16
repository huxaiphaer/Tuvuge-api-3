#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2
import sys
import os

con = None

con = psycopg2.connect(
    "host='localhost' dbname='ride_my_way' user='postgres' password='namungoona'")

#con = psycopg2.connect(
 #   "host='ec2-54-243-253-24.compute-1.amazonaws.com' dbname='d176ms9middb04' user='ycluqmdmwbcxrb' password='c9dee8fe6483f025b2096e72f39c8e1adc835f18635c4f519e14268e40143d33'")


