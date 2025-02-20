import unittest
import asyncio
from echo.agent import Agent

class TestEchoAgent(unittest.TestCase):

    def setUp(self):
        """Initialize a test agent before each test."""
        self.agent = Agent("test_agent")

    def test_register_action_valid(self):
        """Ensure an action registers correctly with required attributes."""
        async def sample_action(args):
            return "Executed"

        self.agent.register_action(
            "test_action",
            sample_action,
            "Test description",
            {"type": "object", "properties": {}},
            {"type": "string"}
        )

        self.assertIn("test_action", self.agent.get_actions())

    def test_register_action_missing_description(self):
        """Ensure registering an action without a description raises an error."""
        async def sample_action(args):
            return "Executed"

        with self.assertRaises(ValueError) as context:
            self.agent.register_action(
                "test_action",
                sample_action,
                None,  # Missing description
                {"type": "object", "properties": {}},
                {"type": "string"}
            )
        self.assertEqual(str(context.exception), "Missing required attributes for action registration")

    def test_register_action_missing_schemas(self):
        """Ensure registering an action without schemas raises an error."""
        async def sample_action(args):
            return "Executed"

        with self.assertRaises(ValueError) as context:
            self.agent.register_action(
                "test_action",
                sample_action,
                "Test description",
                None,  # Missing arguments_schema
                None   # Missing output_schema
            )
        self.assertEqual(str(context.exception), "Missing required attributes for action registration")

    def test_get_action_metadata(self):
        """Ensure actions store metadata correctly."""
        async def sample_action(args):
            return "Executed"

        self.agent.register_action(
            "test_action",
            sample_action,
            "Test description",
            {"type": "object", "properties": {}},
            {"type": "string"}
        )

        action_metadata = self.agent.get_action_metadata("test_action")

        self.assertEqual(action_metadata["description"], "Test description")
        self.assertEqual(action_metadata["arguments_schema"], {"type": "object", "properties": {}})
        self.assertEqual(action_metadata["output_schema"], {"type": "string"})

    def test_invoke_registered_action(self):
        """Ensure invoking a registered action works."""
        async def sample_action(args):
            return f"Received {args}"

        self.agent.register_action(
            "test_action",
            sample_action,
            "Test description",
            {"type": "object", "properties": {}},
            {"type": "string"}
        )

        result = asyncio.run(self.agent.invoke_action("test_action", {"key": "value"}))
        self.assertEqual(result, "Received {'key': 'value'}")

    def test_invoke_unregistered_action(self):
        """Ensure invoking an unregistered action returns an error."""
        result = asyncio.run(self.agent.invoke_action("unknown_action", {}))
        self.assertEqual(result, "Error: Action 'unknown_action' not found")

if __name__ == "__main__":
    unittest.main()