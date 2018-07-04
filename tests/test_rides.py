import json
import datetime
from tests import BaseTestCase

class Tests_Requests(BaseTestCase):
    """Test for requests"""
    def test_rideoffers_submission_successfully(self):
        """Tests when the ride offers  are submitted successfully"""
        with self.client:
            #get token after logging in.
            token = self.get_token()
            response = self.add_ride("Easter offer "+str(datetime.datetime.now()),"Get an offer of 30% of this","Huza","8000",token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data.get('message'), "Ride offer created successfully.")
                    

    def test_get_all_rideoffers(self):
        """Tests when all ride offers are retrieved successfully"""
        with self.client:
           
            #get a token after sign up 
            token = self.get_token()
            res = self.add_ride("Easter offer","Get an offer of 30% of this","Huza","8000",token)
            data = json.loads(res.data.decode())
            response = self.get_rideoffers(token)
            self.assertEqual(response.status_code, 200)

   

   

    def test_gets_all_ride_offers_with_no_token(self):
        """Tests when the no token is provided when getting ride offers """
        with self.client:
            self.register_user("jau", "j@gmail.com", "123456789")
            token = ""
            response = self.add_ride("Easter offer", "Get an offer of 30% of this","Huza", "4000",token)
            response = self.get_rideoffers(token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data.get('message'), "Token is missing")

    def test_gets_all_endpoints_with_expired_token(self):
        """Tests when the token expires when retrieving all endpoints"""
        with self.client:
            self.register_user("jau", "j@gmail.com", "123456789")
            token = "aszdfvkTYOEOODCDBDJVHEDJxwjuHdx dh"
            self.add_ride("Easter offer", "Get an offer of 30% of this","Huza", "4000",token)
            response = self.get_rideoffers(token)
            self.assertEqual(response.status_code, 401)    
   

   


    def test_get_one_rideoffer_with_expired_token(self):
        """Tests when one ride offer is retrieved with expired token"""
        with self.client:
            self.register_user("jau", "j@gmail.com", "123456789")
            token = "zxcvb"
            self.add_ride("Easter offer", "Get an offer of 30% of this", "Huza","4000",token)
            response = self.get_one_rideoffer(token)
            self.assertEqual(response.status_code, 401)

            


   