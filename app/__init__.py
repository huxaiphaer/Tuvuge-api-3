from flask import Flask
from flask_restful import Api
from app.rides.managerides import GetRides, GetSingleRide, CreateRideRequests, GetRideOfferRequests
#from app.user.authentication import Login, SignUp
#from app.rides.request_ride_offer import RequestRideOffer


app = Flask(__name__)

app.secret_key = "huzaifah"
api = Api(app)


#api.add_resource(SignUp, '/api/v1/signup')
#api.add_resource(Login, '/api/v1/login')
api.add_resource(GetRideOfferRequests,'/api/v1/users/rides/<rideId>/requests')
api.add_resource(GetRides, '/api/v1/users/rides')
api.add_resource(GetSingleRide, '/api/v1/rides/<ride_id>')
api.add_resource(CreateRideRequests, '/api/v1/<rideoffer_id>/requests')
