import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from src.routes.chain_routes import create_chain_routes  

class TestChainRoutes(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client and app context."""
        self.app = Flask(__name__)
        self.app.register_blueprint(create_chain_routes(), url_prefix='/api/chain')
        self.client = self.app.test_client()

    @patch('src.routes.chain_routes.create_token')
    @patch('src.routes.chain_routes.create_breadcrumb')
    @patch('src.routes.chain_routes.ChainServices.get_chains')
    def test_get_chains_success(self, mock_get_chains, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/chain for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        mock_chains = [{"id": "chain1", "name": "Test Chain"}]
        mock_get_chains.return_value = mock_chains

        # Act
        response = self.client.get('/api/chain')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_chains)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_get_chains.assert_called_once_with("", mock_token)

    @patch('src.routes.chain_routes.create_token')
    @patch('src.routes.chain_routes.create_breadcrumb')
    @patch('src.routes.chain_routes.ChainServices.get_chains')
    def test_get_chains_failure(self, mock_get_chains, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/chain when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_get_chains.side_effect = Exception("Database error")

        response = self.client.get('/api/chain')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('src.routes.chain_routes.create_token')
    @patch('src.routes.chain_routes.create_breadcrumb')
    @patch('src.routes.chain_routes.ChainServices.get_chain')
    def test_get_chain_success(self, mock_get_chain, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/chain for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        mock_chain = {"id": "chain1", "name": "Test Chain"}
        mock_get_chain.return_value = mock_chain

        # Act
        response = self.client.get('/api/chain/chain1')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_chain)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_get_chain.assert_called_once_with("chain1", mock_token)

    @patch('src.routes.chain_routes.create_token')
    @patch('src.routes.chain_routes.create_breadcrumb')
    @patch('src.routes.chain_routes.ChainServices.get_chain')
    def test_get_chain_failure(self, mock_get_chain, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/chain/{id} when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_get_chain.side_effect = Exception("Database error")

        response = self.client.get('/api/chain/chain1')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

if __name__ == '__main__':
    unittest.main()