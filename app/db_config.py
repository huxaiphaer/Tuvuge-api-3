#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2
import sys


con = None

con = psycopg2.connect(
    "host='localhost' dbname='ride_my_way' user='postgres' password='namungoona'")
