import unittest
import requests


class FlaskTest(unittest.TestCase):

    def test_index(self):
        response = requests.get("http://127.0.0.1:5000/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h2>Use this site to maintain and organize your notes.</h2>' in response.text, True)


if __name__ == " __main__":
    unittest.main()