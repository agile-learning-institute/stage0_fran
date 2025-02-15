import unittest
from flask_utils.token import create_token  # Update to your actual module path


class TestCreateToken(unittest.TestCase):
    def test_create_token(self):
        token = create_token()
        
        # Expected token structure
        expected = {
            "user_id": "aaaa00000000000000000001",
            "roles": ["Staff"]
        }

        self.assertEqual(token, expected)


if __name__ == '__main__':
    unittest.main()