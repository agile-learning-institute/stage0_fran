import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from src.routes.workshop_routes import create_workshop_routes

class TestWorkshopRoutes(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client and app context."""
        self.app = Flask(__name__)
        self.app.register_blueprint(create_workshop_routes(), url_prefix='/api/workshop')
        self.client = self.app.test_client()

    @patch('src.routes.workshop_routes.create_token')
    @patch('src.routes.workshop_routes.create_breadcrumb')
    @patch('src.routes.workshop_routes.WorkshopServices.get_workshops', new_callable=MagicMock)
    def test_get_workshops_success(self, mock_get_workshops, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/workshop for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        mock_workshops = [{"id": "workshop1", "name": "Test Workshop"}]
        mock_get_workshops.return_value = mock_workshops

        # Act
        response = self.client.get('/api/workshop')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_workshops)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_get_workshops.assert_called_once_with("", mock_token)

    @patch('src.routes.workshop_routes.create_token')
    @patch('src.routes.workshop_routes.create_breadcrumb')
    @patch('src.routes.workshop_routes.WorkshopServices.get_workshops')
    def test_get_workshops_failure(self, mock_get_workshops, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/workshop when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_get_workshops.side_effect = Exception("Database error")

        response = self.client.get('/api/workshop')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('src.routes.workshop_routes.create_token')
    @patch('src.routes.workshop_routes.create_breadcrumb')
    @patch('src.routes.workshop_routes.WorkshopServices.get_workshop', new_callable=MagicMock)
    def test_get_workshop_success(self, mock_get_workshop, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/workshop/{id} for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        mock_workshop = {"id": "workshop1", "name": "Test Workshop"}
        mock_get_workshop.return_value = mock_workshop

        # Act
        response = self.client.get('/api/workshop/workshop1')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_workshop)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_get_workshop.assert_called_once_with("workshop1", mock_token)

    @patch('src.routes.workshop_routes.create_token')
    @patch('src.routes.workshop_routes.create_breadcrumb')
    @patch('src.routes.workshop_routes.WorkshopServices.get_workshop')
    def test_get_workshop_failure(self, mock_get_workshop, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/workshop/{id} when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_get_workshop.side_effect = Exception("Database error")

        response = self.client.get('/api/workshop/workshop1')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('src.routes.workshop_routes.create_token')
    @patch('src.routes.workshop_routes.create_breadcrumb')
    @patch('src.routes.workshop_routes.WorkshopServices.add_workshop', new_callable=MagicMock)
    def test_add_workshop_success(self, mock_add_workshop, mock_create_breadcrumb, mock_create_token):
        """Test POST /api/workshop for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        mock_workshop = {"id": "workshop1", "name": "Test Workshop"}
        mock_add_workshop.return_value = mock_workshop
        new_workshop = {"foo":"bar"}

        # Act
        response = self.client.post('/api/workshop', json=new_workshop)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_workshop)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_add_workshop.assert_called_once_with(new_workshop, mock_token)

    @patch('src.routes.workshop_routes.create_token')
    @patch('src.routes.workshop_routes.create_breadcrumb')
    @patch('src.routes.workshop_routes.WorkshopServices.add_workshop')
    def test_add_workshop_failure(self, mock_add_workshop, mock_create_breadcrumb, mock_create_token):
        """Test POST /api/workshop when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_add_workshop.side_effect = Exception("Database error")
        new_workshop = {"foo":"bar"}

        response = self.client.post('/api/workshop', json=new_workshop)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('src.routes.workshop_routes.create_token')
    @patch('src.routes.workshop_routes.create_breadcrumb')
    @patch('src.routes.workshop_routes.WorkshopServices.update_workshop', new_callable=MagicMock)
    def test_update_workshop_success(self, mock_update_workshop, mock_create_breadcrumb, mock_create_token):
        """Test PATCH /api/workshop/{id} for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        mock_workshop = {"id": "workshop1", "foo": "bar"}
        mock_update_workshop.return_value = mock_workshop
        patch_data = {"foo": "bar"}

        # Act
        response = self.client.patch('/api/workshop/workshop1', json=patch_data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_workshop)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_update_workshop.assert_called_once_with("workshop1", mock_token, mock_breadcrumb, patch_data)

    @patch('src.routes.workshop_routes.create_token')
    @patch('src.routes.workshop_routes.create_breadcrumb')
    @patch('src.routes.workshop_routes.WorkshopServices.update_workshop', new_callable=MagicMock)
    def test_update_workshop_failure(self, mock_update_workshop, mock_create_breadcrumb, mock_create_token):
        """Test PATCH /api/workshop/{id} when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_update_workshop.side_effect = Exception("Database error")

        response = self.client.patch('/api/workshop/workshop1', json={})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('src.routes.workshop_routes.create_token')
    @patch('src.routes.workshop_routes.create_breadcrumb')
    @patch('src.routes.workshop_routes.WorkshopServices.start_workshop', new_callable=MagicMock)
    def test_start_workshop_success(self, mock_start_workshop, mock_create_breadcrumb, mock_create_token):
        """Test POST /api/workshop/{id}/start for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        mock_workshop = {"foo":"bar"}
        mock_start_workshop.return_value = mock_workshop

        # Act
        response = self.client.post('/api/workshop/workshop1/start')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_workshop)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_start_workshop.assert_called_once_with("workshop1", mock_token, mock_breadcrumb)

    @patch('src.routes.workshop_routes.create_token')
    @patch('src.routes.workshop_routes.create_breadcrumb')
    @patch('src.routes.workshop_routes.WorkshopServices.start_workshop')
    def test_start_workshop_failure(self, mock_start_workshop, mock_create_breadcrumb, mock_create_token):
        """Test POST /api/workshop/{id}/start when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_start_workshop.side_effect = Exception("Database error")

        response = self.client.post('/api/workshop/workshop1/start')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('src.routes.workshop_routes.create_token')
    @patch('src.routes.workshop_routes.create_breadcrumb')
    @patch('src.routes.workshop_routes.WorkshopServices.advance_workshop', new_callable=MagicMock)
    def test_advance_workshop_success(self, mock_advance_workshop, mock_create_breadcrumb, mock_create_token):
        """Test POST /api/workshop/{id}/next for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        mock_workshop = {"foo":"bar"}
        mock_advance_workshop.return_value = mock_workshop

        # Act
        response = self.client.post('/api/workshop/workshop1/next')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_workshop)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_advance_workshop.assert_called_once_with("workshop1", mock_token, mock_breadcrumb)

    @patch('src.routes.workshop_routes.create_token')
    @patch('src.routes.workshop_routes.create_breadcrumb')
    @patch('src.routes.workshop_routes.WorkshopServices.advance_workshop')
    def test_advance_workshop_failure(self, mock_advance_workshop, mock_create_breadcrumb, mock_create_token):
        """Test POST /api/workshop/{id}/start when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_advance_workshop.side_effect = Exception("Database error")

        response = self.client.post('/api/workshop/workshop1/next')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('src.routes.workshop_routes.create_token')
    @patch('src.routes.workshop_routes.create_breadcrumb')
    @patch('src.routes.workshop_routes.WorkshopServices.add_observation', new_callable=MagicMock)
    def test_add_observation_success(self, mock_add_observation, mock_create_breadcrumb, mock_create_token):
        """Test POST /api/workshop/{id}/observation for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        mock_observation = {"foo":"bar"}
        mock_workshop = {"id": "workshop1", "foo": "bar"}
        mock_add_observation.return_value = mock_workshop

        # Act
        response = self.client.post('/api/workshop/workshop1/observation', json=mock_observation)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_workshop)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_add_observation.assert_called_once_with("workshop1", mock_token, mock_breadcrumb, mock_observation)

    @patch('src.routes.workshop_routes.create_token')
    @patch('src.routes.workshop_routes.create_breadcrumb')
    @patch('src.routes.workshop_routes.WorkshopServices.add_observation', new_callable=MagicMock)
    def test_add_observation_failure(self, mock_add_observation, mock_create_breadcrumb, mock_create_token):
        """Test POST /api/workshop/{id}/observation when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_add_observation.side_effect = Exception("Database error")

        response = self.client.post('/api/workshop/workshop1/observation')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

if __name__ == '__main__':
    unittest.main()