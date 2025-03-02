import json
import unittest
from unittest.mock import MagicMock, patch
from echo.llm_handler import LLMHandler
from echo.message import Message

class TestLLMHandler(unittest.TestCase):
    def setUp(self):
        """Set up a mock LLMHandler instance before each test."""
        self.mock_handle_command = MagicMock()
        self.mock_llm_client = MagicMock()
        self.mock_llm_client.model = "test-model"
        self.llm_handler = LLMHandler(handle_command_function=self.mock_handle_command, llm_client=self.mock_llm_client)

    def test_handle_simple_message(self):
        """Ensure simple agent call falls through."""
        message1 = {"channel_id": "CHANNEL_1", "message":{"role": Message.USER_ROLE, "content": f"{Message.GROUP_DIALOG}:Simple Message"}}
        llm_response = {"role": Message.ASSISTANT_ROLE, "content": "LLM Response"}
        message2 = {"channel_id": "CHANNEL_1", "message":{"role": Message.ASSISTANT_ROLE, "content": f"{Message.GROUP_DIALOG}:LLM Response"}}
        
        self.mock_handle_command.side_effect = [
            [message1],
            llm_response,
            [message1, message2]
        ]
        self.mock_llm_client.chat.return_value = llm_response

        result = self.llm_handler.handle_message(channel="CHANNEL_1", text="Simple Message")

        self.assertEqual(result, "LLM Response")
        self.mock_handle_command.assert_any_call(f"/conversation/add_message/{json.dumps(message1, separators=(',', ':'))}")
        self.mock_handle_command.assert_any_call(f"/conversation/add_message/{json.dumps(message2, separators=(',', ':') )}")
        self.mock_llm_client.chat.assert_called_once()

    def test_llm_reply_format_error(self):
        """Ensure simple agent call falls through."""
        message1 = {"channel_id": "CHANNEL_1", "message":{"role": Message.USER_ROLE, "content": f"{Message.GROUP_DIALOG}:Simple Message"}}
        llm_response = "Just a String"
        
        self.mock_handle_command.side_effect = [
            [message1],
            llm_response
        ]
        self.mock_llm_client.chat.return_value = llm_response

        result = self.llm_handler.handle_message(channel="CHANNEL_1", text="Simple Message")

        self.assertEqual(result, "Just a String")
        self.mock_handle_command.assert_any_call(f"/conversation/add_message/{json.dumps(message1, separators=(',', ':'))}")
        self.mock_llm_client.chat.assert_called_once()

    def test_handle_message_with_agent_call(self):
        """Ensure user making agent call messages are correctly processed."""
        message1 = {"channel_id": "CHANNEL_1", "message":{"role": Message.USER_ROLE, "content": f"{Message.GROUP_DIALOG}:/test_agent/test_action"}}
        agent_response = "Agent Response"
        message2 = {"channel_id": "CHANNEL_1", "message":{"role": Message.ASSISTANT_ROLE, "content": f"{Message.TOOLS_DIALOG}:Agent Response"}}
        llm_response = {"role": Message.ASSISTANT_ROLE, "content": f"{Message.GROUP_DIALOG}:LLM says Agent Response"}
        message3 = {"channel_id": "CHANNEL_1", "message":{"role": Message.ASSISTANT_ROLE, "content": f"{Message.GROUP_DIALOG}:LLM says Agent Response"}}
        
        self.mock_handle_command.side_effect = [
            [message1],
            agent_response,
            [message1, message2],
            llm_response,
            [message1, message2, message3]
        ]
        self.mock_llm_client.chat.return_value = llm_response

        result = self.llm_handler.handle_message(channel="CHANNEL_1", text="/test_agent/test_action")

        self.assertEqual(result, "LLM says Agent Response")
        self.mock_handle_command.assert_any_call("/test_agent/test_action")
        self.mock_handle_command.assert_any_call(f"/conversation/add_message/{json.dumps(message1, separators=(',', ':'))}")
        self.mock_handle_command.assert_any_call(f"/conversation/add_message/{json.dumps(message2, separators=(',', ':') )}")
        self.mock_handle_command.assert_any_call(f"/conversation/add_message/{json.dumps(message3, separators=(',', ':') )}")
        self.mock_llm_client.chat.assert_called_once()

    def test_handle_simple_message_with_recursion(self):
        """Ensure recursive agent call messages are correctly processed."""
        message1 = {"channel_id": "CHANNEL_1", "message":{"role": Message.USER_ROLE, "content": f"{Message.GROUP_DIALOG}:Simple Message"}}
        llm_response = {"role": Message.ASSISTANT_ROLE, "content": f"{Message.TOOLS_DIALOG}:/test_agent/test_action"}
        message2 = {"channel_id": "CHANNEL_1", "message":{"role": Message.ASSISTANT_ROLE, "content": f"{Message.TOOLS_DIALOG}:/test_agent/test_action"}}
        agent_reply = "agent reply 1"
        message3 = {"channel_id": "CHANNEL_1", "message":{"role": Message.ASSISTANT_ROLE, "content": f"{Message.TOOLS_DIALOG}:agent reply 1"}}
        llm_response2 = {"role": Message.ASSISTANT_ROLE, "content": f"{Message.TOOLS_DIALOG}:/test_agent/test_action2"}
        message4 = {"channel_id": "CHANNEL_1", "message":{"role": Message.ASSISTANT_ROLE, "content": f"{Message.TOOLS_DIALOG}:/test_agent/test_action2"}}
        agent_reply2 = "agent reply 2"
        message5 = {"channel_id": "CHANNEL_1", "message":{"role": Message.ASSISTANT_ROLE, "content": f"{Message.TOOLS_DIALOG}:agent reply 2"}}
        llm_response3 = {"role": Message.ASSISTANT_ROLE, "content": f"{Message.GROUP_DIALOG}:LLM Final Answer"}
        message6 = {"channel_id": "CHANNEL_1", "message":{"role": Message.ASSISTANT_ROLE, "content": f"{Message.GROUP_DIALOG}:LLM Final Answer"}}

        self.mock_handle_command.side_effect = [
            [message1],
            [message1, message2],
            agent_reply,
            [message1, message2, message3],
            [message1, message2, message3, message4],
            agent_reply2,
            [message1, message2, message3, message4, message5],
            [message1, message2, message3, message4, message5, message6],
        ]
        self.mock_llm_client.chat.side_effect = [
            llm_response, llm_response2, llm_response3
        ]

        result = self.llm_handler.handle_message(channel="CHANNEL_1", text="Simple Message")

        self.assertEqual(result, "LLM Final Answer")
        self.mock_handle_command.assert_any_call(f"/conversation/add_message/{json.dumps(message1, separators=(',', ':'))}")
        self.mock_handle_command.assert_any_call(f"/conversation/add_message/{json.dumps(message2, separators=(',', ':'))}")
        self.mock_handle_command.assert_any_call(f"/conversation/add_message/{json.dumps(message3, separators=(',', ':'))}")
        self.mock_handle_command.assert_any_call(f"/conversation/add_message/{json.dumps(message4, separators=(',', ':'))}")
        self.mock_handle_command.assert_any_call(f"/conversation/add_message/{json.dumps(message5, separators=(',', ':'))}")
        self.mock_handle_command.assert_any_call(f"/conversation/add_message/{json.dumps(message6, separators=(',', ':'))}")
        self.assertEqual(self.mock_llm_client.chat.call_count, 3)

if __name__ == "__main__":
    unittest.main()
