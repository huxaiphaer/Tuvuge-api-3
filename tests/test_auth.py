import json

from tests import BaseTestCase


class Test_auth(BaseTestCase):
    def test_successful_signup(self):
        """
        Test a user is already exists in the database.
        """
        with self.client:
           
            # Add the same user and see...
            res = self.register_user("jau", "j@gmail.com", "123456789")
            data1 = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertEqual(data1.get('message'), "Sorry,this username is already available.")

    def test_successful_login(self):
        """
        Test a registered user  is logged in successfully through the api
        """
        with self.client:
            self.register_user("jau", "j@gmail.com", "123456789")
            response = self.login_user("jau", "123456789")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data.get('message'),
                             "User logged in successfully")

    def test_wrong_credentials_on_login(self):
        """
        Test a user logs in with wrong credentials
        """
        with self.client:
            self.register_user("jau", "j@gmail.com", "123456789")
            response = self.login_user("dija", "1234509")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data.get('message'),
                             "wrong credentials")

    def test_invalid_username_onsignup(self):
        """Test when a user registers with an invalid username"""
        with self.client:
            response = self.register_user("h", "lol@gmail.com", "12345")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "invalid username, Enter correct username please")
            
    def test_username_with_characters_onsignup(self):
        """Test when a user registers with an invalid username with characters"""
        with self.client:
            response = self.register_user("%2?1@", "ui@gmail.com", "12345")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "Invalid characters not allowed, numbers and symbols are not allowed")

    def test_when_invalid_email_onsignup(self):
        """Test when invalid email is provided onsignup"""
        with self.client:
            response = self.register_user("huz", "hadgmailcom", "123456")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "Enter valid email")

    def test_when_no_password_onsignup(self):
        """Test when no password onsignup"""
        with self.client:
            response = self.register_user("huz", "had@gmail.com", "")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "Enter password")

    def test_when_short_password_onsignup(self):
        """Test when short password is provided onsignup"""
        with self.client:
            response = self.register_user("huz", "had@gmail.com", "12")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "Password is too short, < 5")