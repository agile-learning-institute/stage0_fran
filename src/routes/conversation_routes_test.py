import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from src.routes.conversation_routes import create_conversation_routes  

class TestConversationRoutes(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client and app context."""
        self.app = Flask(__name__)
        self.app.register_blueprint(create_conversation_routes(), url_prefix='/api/conversation')
        self.client = self.app.test_client()

    @patch('src.routes.conversation_routes.create_token')
    @patch('src.routes.conversation_routes.create_breadcrumb')
    @patch('src.routes.conversation_routes.ConversationServices.get_conversations')
    def test_get_conversations_success(self, mock_get_conversations, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/conversation for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_get_conversations.return_value = [{"id": "conversation1", "name": "Test Conversation"}]

        # Act
        response = self.client.get('/api/conversation')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"id": "conversation1", "name": "Test Conversation"}])
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_get_conversations.assert_called_once_with("", mock_token)

    @patch('src.routes.conversation_routes.create_token')
    @patch('src.routes.conversation_routes.create_breadcrumb')
    @patch('src.routes.conversation_routes.ConversationServices.get_conversations')
    def test_get_conversations_failure(self, mock_get_conversations, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/conversation when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_get_conversations.side_effect = Exception("Database error")

        response = self.client.get('/api/conversation')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('src.routes.conversation_routes.create_token')
    @patch('src.routes.conversation_routes.create_breadcrumb')
    @patch('src.routes.conversation_routes.ConversationServices.get_conversation')
    def test_get_conversation_success(self, mock_get_conversation, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/conversation/{id} for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_conversation = {"id": "conversation1", "name": "Test Conversation"}
        mock_get_conversation.return_value = mock_conversation

        # Act
        response = self.client.get('/api/conversation/conversation1')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_conversation)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_get_conversation.assert_called_once_with("conversation1", mock_token)

    @patch('src.routes.conversation_routes.create_token')
    @patch('src.routes.conversation_routes.create_breadcrumb')
    @patch('src.routes.conversation_routes.ConversationServices.get_conversation')
    def test_get_conversation_failure(self, mock_get_conversation, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/conversation/{id} when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_get_conversation.side_effect = Exception("Database error")

        response = self.client.get('/api/conversation/conversation1')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('src.routes.conversation_routes.create_token')
    @patch('src.routes.conversation_routes.create_breadcrumb')
    @patch('src.routes.conversation_routes.ConversationServices.update_conversation', new_callable=MagicMock)
    def test_update_conversation_success(self, mock_update_conversation, mock_create_breadcrumb, mock_create_token):
        """Test PATCH /api/conversation/{id} for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        mock_conversation = {"id": "conversation1", "foo": "bar"}
        mock_update_conversation.return_value = mock_conversation
        patch_data = {"foo": "bar"}

        # Act
        response = self.client.patch('/api/conversation/conversation1', json=patch_data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_conversation)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_update_conversation.assert_called_once_with("conversation1", mock_token, mock_breadcrumb, patch_data)

    @patch('src.routes.conversation_routes.create_token')
    @patch('src.routes.conversation_routes.create_breadcrumb')
    @patch('src.routes.conversation_routes.ConversationServices.update_conversation', new_callable=MagicMock)
    def test_update_conversation_failure(self, mock_update_conversation, mock_create_breadcrumb, mock_create_token):
        """Test PATCH /api/conversation/{id} when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_update_conversation.side_effect = Exception("Database error")

        response = self.client.patch('/api/conversation/conversation1', json={})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('src.routes.conversation_routes.create_token')
    @patch('src.routes.conversation_routes.create_breadcrumb')
    @patch('src.routes.conversation_routes.ConversationServices.add_message')
    def test_add_message_success(self, mock_add_message, mock_create_breadcrumb, mock_create_token):
        """Test POST /api/conversation/{channel_id}/message for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        mock_new_message = "message3"
        mock_messages = ["message1","message2","message3"]
        mock_add_message.return_value = mock_messages

        # Act
        response = self.client.post('/api/conversation/conversation1/message', json=mock_new_message)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_messages)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_add_message.assert_called_once_with("conversation1", mock_token, mock_breadcrumb, mock_new_message)

    @patch('src.routes.conversation_routes.create_token')
    @patch('src.routes.conversation_routes.create_breadcrumb')
    @patch('src.routes.conversation_routes.ConversationServices.add_message')
    def test_add_message_failure(self, mock_add_message, mock_create_breadcrumb, mock_create_token):
        """Test POST /api/conversation/{channel_id}/message when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_add_message.side_effect = Exception("Database error")
        mock_new_message = "message3"

        response = self.client.post('/api/conversation/conversation1/message', json=mock_new_message)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

if __name__ == '__main__':
    unittest.main()