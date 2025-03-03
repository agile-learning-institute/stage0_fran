import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from src.routes.echo_routes import create_echo_routes

class TestEchoRoutes(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client and app context."""
        self.agents = {"agent1":{"actions":[{"action1":{"name":"agent1-action1"}},{"action2":{"name":"agent1-action2"}}]}, 
                       "agent2":{"actions":[{"action1":{"name":"agent2-action1"}},{"action2":{"name":"agent2-action2"}}]}
        }
        self.app = Flask(__name__)
        self.app.register_blueprint(create_echo_routes(self.agents), url_prefix='/api/echo')
        self.client = self.app.test_client()

    @patch('src.routes.echo_routes.create_token')
    @patch('src.routes.echo_routes.create_breadcrumb')
    def test_get_agents_success(self, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/config for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb

        # Act
        response = self.client.get('/api/echo')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, self.agents)
        
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)

    @patch('src.routes.echo_routes.create_token')
    @patch('src.routes.echo_routes.create_breadcrumb')
    def test_get_echo_failure(self, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/echo when an exception is raised."""
        mock_create_token.side_effect = Exception("Token error")
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}

        response = self.client.get('/api/echo')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

if __name__ == '__main__':
    unittest.main()
