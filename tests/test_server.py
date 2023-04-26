import json
import unittest
import os
import sys

# Load the application server to test
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'src'))
from server import app


class ServerTestCase(unittest.TestCase):
    # Class to perform the tests

    def setUp(self):
        #  Initiate the class test
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

        # User template
        self.user = {"first_name": "new", "last_name": "user", "department": "cyberAck"}

    def tearDown(self):
        self.ctx.pop()

    def test_root(self):
        # Test the function: root
        response = self.client.get("/")
        self.assertTrue(response.status_code == 200)
        self.assertTrue("Hello world" in response.text)

    def test_get_user_by_id(self):
        # Test the function: get_user_by_id
        for i_user in range(1, 5):
            response = self.client.get(f"/user/{i_user}")
            self.assertTrue(response.status_code == 200)

            data = json.loads(response.text)
            self.assertIsInstance(data["department"], str)
            self.assertIsInstance(data["first_name"], str)
            self.assertIsInstance(data["last_name"], str)
            self.assertIsInstance(data["uid"], int)

    def test_create_user(self):
        # Test the function: create_user
        params = "&".join([f"{i_user}={self.user[i_user]}" for i_user in self.user])
        response = self.client.post(f"/user?{params}")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(json.loads(response.text)["uid"] == 6)

    def test_update_user_by_id(self):
        # Test the function: update_user_by_id
        user = json.loads(self.client.get(f"/user/1").text)
        user["first_name"] = "updated"
        params = "&".join([f"{i_user}={user[i_user]}" for i_user in user])
        response = self.client.put(f"/user/{user['uid']}?{params}")

        self.assertTrue(response.status_code == 200)
        self.assertTrue(json.loads(response.text)["uid"] == 1)

    def test_delete_user(self):
        # Test the function: delete_user
        response = self.client.delete("/user/6")
        self.assertTrue(response.status_code == 200)
        self.assertTrue("ok" in response.text)

    def test_list_user(self):
        # Test the function: list_user
        response = self.client.get("/users")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(json.loads(response.text)) == 5)


if __name__ == "__main__":
    unittest.main()
