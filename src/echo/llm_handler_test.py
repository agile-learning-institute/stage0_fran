import unittest
from unittest.mock import MagicMock, patch
from echo.llm_handler import LLMHandler

class TestLLMHandler(unittest.TestCase):
    def setUp(self):
        """Set up a mock LLMHandler instance before each test."""
        self.mock_handle_command = MagicMock()
        self.mock_llm_client = MagicMock()
        self.mock_llm_client.model = "test-model"
        self.llm_handler = LLMHandler(handle_command_function=self.mock_handle_command, llm_client=self.mock_llm_client)

    @patch("echo.llm_handler.logging.debug")
    def test_handle_message_with_agent_call(self, mock_debug):
        """Ensure agent call messages are correctly processed."""
        self.mock_handle_command.side_effect = [
            [{"from": "user", "to": "external", "content": "Hello"}],  # Mock conversation update
            "Agent Response",  # Mock agent reply
            [{"from": "agent", "to": "internal", "content": "Agent Response"}],  # Agent reply added
            "LLM Response"  # Mock LLM response
        ]
        self.mock_llm_client.chat.return_value = "LLM Response"

        result = self.llm_handler.handle_message("Alice", "general", "/test_agent/test_action")

        self.assertEqual(result, "LLM Response")
        self.mock_handle_command.assert_any_call("/test_agent/test_action")
        self.mock_llm_client.chat.assert_called_once()

    @patch("echo.llm_handler.logging.debug")
    def test_handle_message_without_agent_call(self, mock_debug):
        """Ensure normal user messages are processed without agent interaction."""
        self.mock_handle_command.return_value = [{"from": "user", "to": "external", "content": "Hello"}]
        self.mock_llm_client.chat.return_value = "LLM Response"

        result = self.llm_handler.handle_message("Alice", "general", "Hello")

        self.assertEqual(result, "LLM Response")
        self.mock_llm_client.chat.assert_called_once()
        self.mock_handle_command.assert_called_once()

if __name__ == "__main__":
    unittest.main()
