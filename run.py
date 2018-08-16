from flask import Flask, redirect
from flask_restful import Resource, Api
from app import app

@app.route('/',methods=['GET'])
def index():
    return redirect("https://tuvugeapi.docs.apiary.io/#",code=302)
if __name__ == '__main__':
    app.run(port=5001,debug=True)