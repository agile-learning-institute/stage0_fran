import unittest
from unittest.mock import patch
from echo.llm_handler import LLMHandler
from echo.echo import Echo
from echo.ollama_llm_client import OllamaLLMClient

class TestLLMHandler(unittest.TestCase):

    def setUp(self):
        """Initialize LLMHandler with mocked dependencies."""
        self.echo = Echo()
        self.llm_client = OllamaLLMClient()
        self.llm_handler = LLMHandler(self.echo, self.llm_client)

    @patch.object(Echo, 'handle_command')
    @patch.object(OllamaLLMClient, 'chat')
    def test_handle_message_with_agent_call(self, mock_chat, mock_handle_command):
        """Ensure agent call messages are correctly processed."""
        
        mock_handle_command.side_effect = [
            "Agent Response",  # Agent call
            [{"from": "agent", "to": "internal", "content": "Agent Response"}],  # Internal message from agent
            [{"from": "system", "to": "external", "content": "LLM Response"}],  # LLM final response
            [{"from": "system", "to": "external", "content": "LLM Response"}]  # Ensures enough responses
        ]
        
        mock_chat.return_value = "LLM Response"

        result = self.llm_handler.handle_message("Alice", "general", "/test_agent/test_action")

        self.assertEqual(result, "LLM Response")
        mock_handle_command.assert_any_call("/test_agent/test_action")
        mock_chat.assert_called_once()
    
    @patch.object(Echo, 'handle_command')
    @patch.object(OllamaLLMClient, 'chat')
    def test_handle_message_internal_llm_response(self, mock_chat, mock_handle_command):
        """Ensure internal LLM responses are processed recursively."""
        mock_handle_command.side_effect = [
            [{"from": "Alice", "to": "external", "content": "Query"}],  # User message added
            [{"from": "system", "to": "internal", "content": "/test_agent/test_action"}],  # LLM internal response
            "Agent Response",  # Agent reply
            [{"from": "agent", "to": "internal", "content": "Agent Response"}],  # Agent response added
            [{"from": "system", "to": "external", "content": "Final LLM Response"}]  # LLM response added
        ]
        mock_chat.side_effect = [
            {"from": "system", "to": "internal", "content": "/test_agent/test_action"},
            "Final LLM Response"
        ]

        result = self.llm_handler.handle_message("Alice", "general", "Query")

        self.assertEqual(result, "Final LLM Response")
        mock_handle_command.assert_any_call("/test_agent/test_action")
        mock_chat.assert_called()

    @patch.object(Echo, 'handle_command')
    @patch.object(OllamaLLMClient, 'chat')
    def test_handle_message_normal_text(self, mock_chat, mock_handle_command):
        """Ensure normal messages update conversation and trigger LLM."""
        mock_handle_command.side_effect = [
            [{"from": "Alice", "to": "external", "content": "Hello"}],  # User message added
            [{"from": "system", "to": "external", "content": "LLM Response"}]  # LLM response added
        ]
        mock_chat.return_value = "LLM Response"

        result = self.llm_handler.handle_message("Alice", "general", "Hello")

        self.assertEqual(result, "LLM Response")
        mock_chat.assert_called_once()

if __name__ == "__main__":
    unittest.main()