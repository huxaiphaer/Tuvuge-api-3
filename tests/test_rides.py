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

    def test_no_token_submit_ride_offers(self):
            token = ""
            response = self.add_ride("Easter offer "+str(datetime.datetime.now()),"Get an offer of 30% of this","Huza","8000",token)
            json.loads(response.data.decode())
            self.assertEqual(response.status_code,  401)

    def test_expired_token_ride_offers(self):
            token = ""
            response = self.add_ride("Easter offer "+str(datetime.datetime.now()),"Get an offer of 30% of this","Huza","8000",token)
            json.loads(response.data.decode())
            self.assertEqual(response.status_code,  401)

    def test_already_available_ride_ride_offer(self):
            token = self.get_token()
            self.add_ride("Easter offer ","Get an offer of 30% of this","Huza","8000",token)
            res = self.add_ride("Easter offer ","Get an offer of 30% of this","Huza","8000",token)
            json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            

            

                    

    def test_get_all_rideoffers(self):
        """Tests when all ride offers are retrieved successfully"""
        with self.client:
           
            #get a token after sign up 
            token = self.get_token()
            res = self.add_ride("Easter offer","Get an offer of 30% of this","Huza","8000",token)
            json.loads(res.data.decode())
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

    def test_get_one_rideoffer_with_no_token(self):
        """Tests when one ride offer is retrieved with expired token"""
        with self.client:
           
            token = ""
            self.add_ride("Easter offer", "Get an offer of 30% of this", "Huza","4000",token)
            response = self.get_one_rideoffer(token)
            self.assertEqual(response.status_code, 401)


    def test_un_available_ride_offer(self):
        """test un available ride offers"""
        with self.client:
            token = self.get_token()
            res= self.client.get('/api/v1/rides/200',headers=({"token": token}))
            #print(res.data)
            json.loads(res.data.decode())
            self.assertEqual(res.status_code, 404)
          

    

    def test_no_token_get_one_ride_req(self):
        """Test no token get one ride request"""
        token = ""
        res= self.client.get('/api/v1/users/rides/5/requests', 
        content_type='application/json',headers=({"token": token}))
        json.loads(res.data.decode())
        self.assertEqual(res.status_code,401)
            
    
    def test_expired_token(self):
        """Test expired token"""
        token = "aWOnejbf"
        res= self.client.get('/api/v1/users/rides/5/requests', 
        content_type='application/json',headers=({"token": token}))
        json.loads(res.data.decode())
        self.assertEqual(res.status_code,401)



    def test_no_token_while_creating_requests(self):
        """test no token while creating requests"""
        with self.client:
            #/api/v1/9/requests
            res= self.client.post('/api/v1/9/requests',headers=({"token": ""}))
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code,401)
            self.assertEqual(data.get('message'), "Token is missing")

    def test_no_token_getting_ride_requests(self):
        """Tests with no token gettiing request"""
        with self.client:
            res= self.client.post('/api/v1/1/requests',headers=({"token": ""}))
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code,401)
            self.assertEqual(data.get('message'), "Token is missing")

    def test_no_ride_requests_found(self):
        """Tests no ride requests found"""
        token = self.get_token()
        res= self.client.post('/api/v1/190/requests',headers=({"token": token}))
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,404)
        self.assertEqual(data.get('message'), "sorry please , ride offer not found")

    def test_no_token_accepting_or_rejecting(self):
        """Test no token accepting or rejecting"""
        res= self.client.put('/api/v1/users/rides/1/requests/1', data=json.dumps(dict(status=0)),
        content_type='application/json',headers=({"token": ""}))
        data=json.loads(res.data.decode())
        self.assertEqual(res.status_code,401)
        self.assertEqual(data.get('message'), "Token is missing")

  


    def test_accepting_ride_offer(self):
        """Test accepting ride offer"""
        token = self.get_token()
        res= self.client.put('/api/v1/users/rides/1/requests/1', data=json.dumps(dict(status=1)),
        content_type='application/json',headers=({"token": token}))
        json.loads(res.data.decode())
        self.assertEqual(res.status_code,200)

   
       




            



    


            


   