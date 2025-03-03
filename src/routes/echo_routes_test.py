import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from echo.echo import Echo
from routes.echo_routes import create_echo_routes

class TestEchoRoutes(unittest.TestCase):
    
    def setUp(self):
        """Set up the Flask test client and mock Echo instance."""
        self.mock_echo = MagicMock(spec=Echo)

        self.app = Flask(__name__)
        self.app.register_blueprint(create_echo_routes(self.mock_echo), url_prefix='/api/echo')
        self.client = self.app.test_client()

    @patch('routes.echo_routes.create_token')
    @patch('routes.echo_routes.create_breadcrumb')
    def test_get_agents_success(self, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/echo for successful response."""
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}

        self.mock_echo.get_agents.return_value = ["agent1", "agent2"]

        response = self.client.get('/api/echo')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, ["agent1", "agent2"])
        
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        self.mock_echo.get_agents.assert_called_once()

    @patch('routes.echo_routes.create_token')
    @patch('routes.echo_routes.create_breadcrumb')
    def test_get_agents_failure(self, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/echo when an exception occurs."""
        mock_create_token.side_effect = Exception("Token error")
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}

        response = self.client.get('/api/echo')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_not_called()
        self.mock_echo.get_agents.assert_not_called()

    @patch('routes.echo_routes.create_token')
    @patch('routes.echo_routes.create_breadcrumb')
    def test_get_agent_success(self, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/echo/<name> for a successful agent retrieval."""
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}

        self.mock_echo.get_agent.return_value = {"name": "agent1", "actions": ["action1", "action2"]}

        response = self.client.get('/api/echo/agent1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"name": "agent1", "actions": ["action1", "action2"]})

        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        self.mock_echo.get_agent.assert_called_once_with(agent_name="agent1")

    @patch('routes.echo_routes.create_token')
    @patch('routes.echo_routes.create_breadcrumb')
    def test_get_agent_failure(self, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/echo/<name> when an exception occurs."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}

        self.mock_echo.get_agent.side_effect = Exception("Database error")

        response = self.client.get('/api/echo/agent1')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with({"user_id": "mock_user"})
        self.mock_echo.get_agent.assert_called_once_with(agent_name="agent1")

if __name__ == '__main__':
    unittest.main()