from flask import Flask
from flask_restful import Resource, Api
from app import app

@app.route('/', methods=['GET'])
def index():
    return ('Welcome to  Tuvuge  API. Test the endpoints in postman')

if __name__ == '__main__':
    app.run(port=5000,debug=True)