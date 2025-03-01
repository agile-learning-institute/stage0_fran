import unittest
from echo.message import Message

class TestMessage(unittest.TestCase):

    def test_constructor_message(self):
        """ """        
        output = Message(message={"role":"user", "content": "group:Hi"})
        self.assertEqual(output.role, "user")
        self.assertEqual(output.dialog, "group")
        self.assertEqual(output.content, "Hi")

    def test_constructor_parts(self):
        """ """
        output = Message(role="assistant", dialog="tools", content="Hello")
        self.assertEqual(output.role, "assistant")
        self.assertEqual(output.dialog, "tools")
        self.assertEqual(output.content, "Hello")

    def test_get_LLM_Message(self):
        """ """
        message = Message(role="assistant", dialog="group", content="How can I help")
        llm_message = {"role": "assistant", "content": "group:How can I help"}
        self.assertEqual(message.get_llm_message(), llm_message)

if __name__ == "__main__":
    unittest.main()