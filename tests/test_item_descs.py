from app import create_app
from app.models import db
import unittest

class TestItemDesc(unittest.TestCase):
    def setUp(self):  # ------------------------------------------------------ ItemDesc Setup
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def test_create_item_desc(self):  # ------------------------------------------------------ Create Item Test Passed 🙂
        payload = {
            "name": "Oil Filter",
            "price": 29.99
        }

        response = self.client.post('/item_descs/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Oil Filter")
        self.assertEqual(response.json['price'], 29.99)

    def test_create_duplicate_item_desc(self):  # ------------------------------------------------------ Duplicate Item Test Passed 🙂
        payload = {
            "name": "Oil Filter",
            "price": 29.99
        }

        self.client.post('/item_descs/', json=payload)
        duplicate_response = self.client.post('/item_descs/', json=payload)
        self.assertEqual(duplicate_response.status_code, 400)
        self.assertEqual(duplicate_response.json['error'], "Item already exists.")

    def test_get_all_item_descs(self):  # ------------------------------------------------------ Get All Item Test Passed 🙂
        payload = {
            "name": "Air Filter",
            "price": 15.49
        }

        self.client.post('/item_descs/', json=payload)
        response = self.client.get('/item_descs/')
        self.assertEqual(response.status_code, 200)

        items_list = response.get_json()
        item_exists = False

        for item in items_list:
            if item['name'] == "Air Filter":
                item_exists = True
                break

        self.assertTrue(item_exists)

    def test_get_item_desc_by_id(self):  # ------------------------------------------------------ Get Item By ID Test Passed 🙂
        payload = {
            "name": "Brake Pads",
            "price": 89.99
        }

        post_response = self.client.post('/item_descs/', json=payload)
        item_id = post_response.get_json()['id']

        get_response = self.client.get(f'/item_descs/{item_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.get_json()['name'], "Brake Pads")

    def test_update_item_desc(self):  # ------------------------------------------------------ Update Item Test Passed 🙂
        original = {
            "name": "Cabin Filter",
            "price": 17.75
        }

        updated = {
            "name": "Cabin Filter XL",
            "price": 22.99
        }

        post_response = self.client.post('/item_descs/', json=original)
        item_id = post_response.get_json()['id']

        put_response = self.client.put(f'/item_descs/{item_id}', json=updated)
        self.assertEqual(put_response.status_code, 200)

        updated_data = put_response.get_json()
        self.assertEqual(updated_data['name'], "Cabin Filter XL")
        self.assertEqual(updated_data['price'], 22.99)

    def test_delete_item_desc(self):  # ------------------------------------------------------ Delete Item Test Passed 🙂
        payload = {
            "name": "Timing Belt",
            "price": 120.00
        }

        post_response = self.client.post('/item_descs/', json=payload)
        item_id = post_response.get_json()['id']

        delete_response = self.client.delete(f'/item_descs/{item_id}')
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn("Item Deleted", delete_response.get_data(as_text=True))

    def test_search_item_desc(self):  # ------------------------------------------------------ Search Item Test Passed 🙂
        payload = {
            "name": "Alternator",
            "price": 199.99
        }

        self.client.post('/item_descs/', json=payload)

        search_response = self.client.get('/item_descs/search?item=Alternator')
        self.assertEqual(search_response.status_code, 200)

        data = search_response.get_json()
        self.assertEqual(data['item']['name'], "Alternator")
        self.assertEqual(data['stock'], 0)  
