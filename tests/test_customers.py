from app import create_app
from app.models import db
import unittest

class TestCustomer(unittest.TestCase):
    def setUp(self):    #------------------------------------------------------ Customer Setup
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def test_create_customer(self): #------------------------------------------------------ Create Customer Test Passed 🙂
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "661-202-9461"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")

    def test_invalid_creation(self):    #------------------------------------------------------ Invalid Create Customer Test Passed 🙂
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com"
        }

        response = self.client.post('/customers/',json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['phone'],['Missing data for required field.'])

    def test_get_customers(self):   #------------------------------------------------------ Get Customers Test Passed 🙂
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "661-202-9461"
        }

        response_post = self.client.post('/customers/', json=customer_payload)  # --- Creating the client 1st
        self.assertEqual(response_post.status_code, 201)

        response_get = self.client.get('/customers/')   # --- Sending GET
        self.assertEqual(response_get.status_code, 200)

        data = response_get.get_json()  # --- Getting the response_get and making it into a python list of dictionaries 

        customer_exists = False

        for customer in data:   # --- Something I'm good at :)
            if customer['name'] == "John Doe":
                customer_exists = True
                break 
        self.assertTrue

