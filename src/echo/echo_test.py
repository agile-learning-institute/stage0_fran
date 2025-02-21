import unittest
import json
from echo.echo import Echo
from echo.agent import Agent
from unittest.mock import Mock

class TestEcho(unittest.TestCase):

    def setUp(self):
        """Initialize Echo instance before each test."""
        self.echo = Echo()
        self.agent = Mock(spec=Agent)
        self.agent.get_actions.return_value = ["test_action"]
        self.agent.invoke_action.return_value = "Action executed successfully"
        self.echo.register_agent("test_agent", self.agent)

    def test_register_agent(self):
        """Ensure an agent is registered successfully."""
        self.assertIn("test_agent", self.echo.get_agents())

    def test_register_invalid_agent(self):
        """Ensure registering a non-Agent instance raises an error."""
        with self.assertRaises(ValueError):
            self.echo.register_agent("invalid_agent", "not_an_agent")

    def test_parse_command_valid(self):
        """Ensure a valid command is parsed correctly."""
        command = "/test_agent/test_action/{\"key\": \"value\"}"
        agent, action, arguments = self.echo.parse_command(command)

        self.assertEqual(agent, "test_agent")
        self.assertEqual(action, "test_action")
        self.assertEqual(arguments, {"key": "value"})

    def test_parse_command_invalid_json(self):
        """Ensure command with invalid JSON raises an exception."""
        command = "/test_agent/test_action/{invalid_json}"
        with self.assertRaises(Exception):
            self.echo.parse_command(command)

    def test_handle_command_valid(self):
        """Ensure a valid command is routed correctly."""
        command = "/test_agent/test_action/{\"key\": \"value\"}"
        result = self.echo.handle_command(command)
        
        self.assertEqual(result, "Action executed successfully")
        self.agent.invoke_action.assert_called_once_with("test_action", {"key": "value"})

    def test_handle_command_unknown_agent(self):
        """Ensure an unknown agent returns silence."""
        command = "/unknown_agent/test_action/{\"key\": \"value\"}"
        result = self.echo.handle_command(command)

        self.assertEqual(result, "")

    def test_handle_command_unknown_action(self):
        """Ensure an unknown action returns available actions."""
        command = "/test_agent/unknown_action/{}"
        result = self.echo.handle_command(command)

        self.assertIn("Unknown action 'unknown_action'", result)
        self.assertIn("Available actions: test_action", result)

if __name__ == "__main__":
    unittest.main()
