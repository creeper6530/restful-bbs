# HUGE credit to ChatGPT. I just uploaded the documentation and after mere few minutes, the unit test porgram was ready to run!

import unittest
import requests
from os import system

class TestAPIEndpoints(unittest.TestCase):

    base_url = "http://127.0.0.1:5000"  # Replace with your actual API base URL

    # Test GET /boards
    def test_get_boards(self):
        response = requests.get(f"{self.base_url}/boards")
        self.assertEqual(response.status_code, 200)
        boards = response.json()
        self.assertIsInstance(boards, list)

    # Test POST /boards
    def test_add_board(self):
        data = {
            "name": "TestBoard",
            "token": "S4mpl3T0k3n"
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{self.base_url}/boards", json=data, headers=headers)
        self.assertEqual(response.status_code, 204)

    # Test DELETE /boards
    def test_delete_board(self):
        data = {
            "name": "TestBoard",
            "token": "S4mpl3T0k3n"
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.delete(f"{self.base_url}/boards", json=data, headers=headers)
        self.assertEqual(response.status_code, 204)

    # Test GET /boards/<board>
    def test_get_posts_from_board(self):
        response = requests.get(f"{self.base_url}/boards/Tech")
        self.assertEqual(response.status_code, 200)
        posts = response.json()
        self.assertIsInstance(posts, list)

    # Test POST /boards/<board>
    def test_add_post_to_board(self):
        data = {
            "title": "Test",
            "contents": "Random article",
            "token": "S4mpl3T0k3n"
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{self.base_url}/boards/Tech", json=data, headers=headers)
        self.assertEqual(response.status_code, 204)

    # Test DELETE /boards/<board>
    def test_delete_post_from_board(self):
        data = {
            "id": requests.get(f"{self.base_url}/boards/Tech").json()[-1]["id"], # ID of the last added post
            "token": "S4mpl3T0k3n"
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.delete(f"{self.base_url}/boards/Tech", json=data, headers=headers)
        self.assertEqual(response.status_code, 204)

    # Add more tests for other endpoints as needed



class TestAuthEndpoints(unittest.TestCase):

    base_url = "http://127.0.0.1:5000"

    # Test POST /auth/login
    def test_login(self):
        data = {
            "username": "guest1",
            "password": "qwerty"
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{self.base_url}/auth/login", json=data, headers=headers)
        self.assertEqual(response.status_code, 201)
        token_response = response.json()
        self.assertTrue("token" in token_response)

    # Test POST /auth/logout
    def test_logout(self):
        data = {
            "token": requests.post(f"{self.base_url}/auth/login", json={"username": "guest1","password": "qwerty"}, headers={'Content-Type': 'application/json'}).json()["token"]
            # Obtains a token to try to log out by the already tested login endpoint
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{self.base_url}/auth/logout", json=data, headers=headers)
        self.assertEqual(response.status_code, 204)

    # Test POST /auth/logout_all
    def test_logout_all(self):
        data = {
            "token": requests.post(f"{self.base_url}/auth/login", json={"username": "guest1","password": "qwerty"}, headers={'Content-Type': 'application/json'}).json()["token"]
            # Obtains a token to try to log out by the already tested login endpoint
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{self.base_url}/auth/logout_all", json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        logout_count = response.json()
        self.assertTrue("number" in logout_count)

    # Test POST /auth/register
    def test_register(self):
        data = {
            "username": "test",
            "password": "somepasswd"
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{self.base_url}/auth/register", json=data, headers=headers)
        self.assertEqual(response.status_code, 204)

    # Test POST /auth/chpasswd
    def test_change_password(self):
        data = {
            "username": "test",
            "old_password": "somepasswd",
            "new_password": "anotherpasswd"
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{self.base_url}/auth/chpasswd", json=data, headers=headers)
        self.assertEqual(response.status_code, 204)

    # Test POST /auth/unregister
    def test_unregister(self):
        data = {
            "username": "test",
            "password": "anotherpasswd"
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{self.base_url}/auth/unregister", json=data, headers=headers)
        self.assertEqual(response.status_code, 204)

    # Add more tests for other auth endpoints as needed

if __name__ == '__main__':
    if input("Do you want to start the Dockerized app (Y/N)? ").upper() == "Y":
        system("docker compose up --wait")
    

    suite = unittest.TestSuite()
    suite.addTest(TestAPIEndpoints('test_get_boards'))
    suite.addTest(TestAPIEndpoints('test_add_board'))
    suite.addTest(TestAPIEndpoints('test_delete_board'))

    suite.addTest(TestAPIEndpoints('test_get_posts_from_board'))
    suite.addTest(TestAPIEndpoints('test_add_post_to_board'))
    suite.addTest(TestAPIEndpoints('test_delete_post_from_board'))
    
    suite.addTest(TestAuthEndpoints('test_login'))
    suite.addTest(TestAuthEndpoints('test_logout'))
    suite.addTest(TestAuthEndpoints('test_logout_all'))

    suite.addTest(TestAuthEndpoints('test_register'))
    suite.addTest(TestAuthEndpoints('test_change_password'))
    suite.addTest(TestAuthEndpoints('test_unregister'))

    # Run the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)