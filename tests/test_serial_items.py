from app import create_app
from app.models import db
import unittest

class TestSerialItem(unittest.TestCase):
    def setUp(self):  # ------------------------------------------------------ SerialItem Setup
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def test_create_serial_item_valid_desc(self):  # ------------------------------------------------------ Create SerialItem Test Passed 🙂
        desc_payload = {
            "name": "Battery",
            "price": 149.99
        }

        post_desc = self.client.post('/item_descs/', json=desc_payload)
        self.assertEqual(post_desc.status_code, 201)

        item_desc_id = post_desc.get_json()['id']

        post_serial = self.client.post(f'/serial_items/{item_desc_id}')
        self.assertEqual(post_serial.status_code, 201)

        data = post_serial.get_json()
        self.assertEqual(data['description']['name'], "Battery")

    def test_create_serial_item_invalid_desc(self):  # ------------------------------------------------------ Invalid Description ID Test Passed 🙂
        response = self.client.post('/serial_items/55')
        self.assertEqual(response.status_code, 200) 

        error_msg = response.get_json()
        self.assertIn("error", error_msg)
        self.assertEqual(error_msg['error'], "Invalid 55")

    def test_get_all_serial_items(self):  # ------------------------------------------------------ Get All SerialItems Test Passed 🙂
        desc_payload = {
            "name": "Radiator",
            "price": 89.50
        }

        post_desc = self.client.post('/item_descs/', json=desc_payload)
        item_desc_id = post_desc.get_json()['id']

        self.client.post(f'/serial_items/{item_desc_id}')
        self.client.post(f'/serial_items/{item_desc_id}')

        get_response = self.client.get('/serial_items/')
        self.assertEqual(get_response.status_code, 200)

        serial_items_list = get_response.get_json()

        serial_items_exist = 0

        for item in serial_items_list:
            if item['description']['name'] == "Radiator":
                serial_items_exist = serial_items_exist + 1

        self.assertEqual(serial_items_exist, 2)

    def test_delete_serial_item_valid(self):  # ------------------------------------------------------ Delete SerialItem Test Passed 🙂
        desc_payload = {
            "name": "Spark Plug",
            "price": 12.75
        }

        post_desc = self.client.post('/item_descs/', json=desc_payload)
        item_desc_id = post_desc.get_json()['id']

        post_serial = self.client.post(f'/serial_items/{item_desc_id}')
        serial_id = post_serial.get_json()['id']

        delete_response = self.client.delete(f'/serial_items/{serial_id}')
        self.assertEqual(delete_response.status_code, 200)

        message = delete_response.get_data(as_text=True)
        self.assertIn("Deleted Item: Spark Plug", message)

    def test_delete_serial_item_invalid(self):  # ------------------------------------------------------ Delete Invalid SerialItem Test Passed 🙂
        delete_response = self.client.delete('/serial_items/45')
        self.assertEqual(delete_response.status_code, 404)

        error_msg = delete_response.get_json()
        self.assertIn("error", error_msg)
        self.assertEqual(error_msg["error"], "Serial ID does not exist.")
