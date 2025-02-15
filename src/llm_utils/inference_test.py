import unittest
from unittest.mock import patch, MagicMock
from llm_utils.inference import Inference  # Update this path to your actual module


class TestInference(unittest.TestCase):
    @patch('llm_utils.inference.ollama.chat')  # Patch the ollama.chat method
    def test_chat(self, mock_chat):
        # Arrange: Setup mock response
        mock_response = MagicMock()
        mock_response.message.content = "Hello, world!"
        mock_chat.return_value = mock_response

        model = "llama3.2:latest"
        messages = [{"role": "user", "content": "Hi there!"}]

        # Act: Call Inference.chat
        response = Inference.chat(self, model, messages)

        # Assert: Verify the output
        mock_chat.assert_called_once_with(model=model, messages=messages)
        self.assertEqual(response.message.content, "Hello, world!")


if __name__ == '__main__':
    unittest.main()