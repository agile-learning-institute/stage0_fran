import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from src.routes.exercise_routes import create_exercise_routes  

class TestExerciseRoutes(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client and app context."""
        self.app = Flask(__name__)
        self.app.register_blueprint(create_exercise_routes(), url_prefix='/api/exercise')
        self.client = self.app.test_client()

    @patch('src.routes.exercise_routes.create_token')
    @patch('src.routes.exercise_routes.create_breadcrumb')
    @patch('src.routes.exercise_routes.ExerciseServices.get_exercises')
    def test_get_exercises_success(self, mock_get_exercises, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/exercise for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        mock_exercises = [{"id": "exercise1", "name": "Test Exercise"}]
        mock_get_exercises.return_value = mock_exercises

        # Act
        response = self.client.get('/api/exercise')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_exercises)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_get_exercises.assert_called_once_with("", mock_token)

    @patch('src.routes.exercise_routes.create_token')
    @patch('src.routes.exercise_routes.create_breadcrumb')
    @patch('src.routes.exercise_routes.ExerciseServices.get_exercises')
    def test_get_exercises_failure(self, mock_get_exercises, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/exercise when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_get_exercises.side_effect = Exception("Database error")

        response = self.client.get('/api/exercise')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('src.routes.exercise_routes.create_token')
    @patch('src.routes.exercise_routes.create_breadcrumb')
    @patch('src.routes.exercise_routes.ExerciseServices.get_exercise')
    def test_get_exercise_success(self, mock_get_exercise, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/exercise for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        mock_exercise = {"id": "exercise1", "name": "Test Exercise"}
        mock_get_exercise.return_value = mock_exercise

        # Act
        response = self.client.get('/api/exercise/exercise1')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_exercise)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_get_exercise.assert_called_once_with("exercise1", mock_token)

    @patch('src.routes.exercise_routes.create_token')
    @patch('src.routes.exercise_routes.create_breadcrumb')
    @patch('src.routes.exercise_routes.ExerciseServices.get_exercise')
    def test_get_exercise_failure(self, mock_get_exercise, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/exercise/{id} when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_get_exercise.side_effect = Exception("Database error")

        response = self.client.get('/api/exercise/exercise1')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

if __name__ == '__main__':
    unittest.main()