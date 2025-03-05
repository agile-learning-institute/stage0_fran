import unittest
from echo.message import Message

class TestMessage(unittest.TestCase):

    def test_constructor_message(self):
        """Test message based constructor with valid message"""        
        message = Message(message={"role":Message.SYSTEM_ROLE, "content": f"{Message.TOOLS_DIALOG}:Hi"})
        self.assertEqual(message.role, Message.SYSTEM_ROLE)
        self.assertEqual(message.dialog, Message.TOOLS_DIALOG)
        self.assertEqual(message.content, "Hi")

    def test_construct_message_string(self):
        """Test message based constructor with string message"""
        message = Message("just a string")
        self.assertEqual(message.dialog, Message.GROUP_DIALOG)
        self.assertEqual(message.role, Message.USER_ROLE)
        self.assertEqual(message.content, "just a string")

    def test_construct_message_missing_role(self):
        """Test message based constructor with message without a role"""
        message = Message({"content":f"{Message.TOOLS_DIALOG}:Hi"})
        self.assertEqual(message.dialog, Message.TOOLS_DIALOG)
        self.assertEqual(message.role, Message.USER_ROLE)
        self.assertEqual(message.content, "Hi")

    def test_construct_message_missing_content(self):
        """Test message based constructor with message without content"""
        message = Message({"role": Message.SYSTEM_ROLE})
        self.assertEqual(message.dialog, Message.GROUP_DIALOG)
        self.assertEqual(message.role, Message.SYSTEM_ROLE)
        self.assertEqual(message.content, "")

    def test_constructor_parts(self):
        """Test part based constructor with valid input """
        message = Message(role=Message.SYSTEM_ROLE, dialog=Message.TOOLS_DIALOG, content="Hello")
        self.assertEqual(message.role, Message.SYSTEM_ROLE)
        self.assertEqual(message.dialog, Message.TOOLS_DIALOG)
        self.assertEqual(message.content, "Hello")
        
    def test_construct_parts_missing_role(self):
        """Test parameter based constructor without a role"""
        message = Message(dialog=Message.TOOLS_DIALOG, content="Hello")
        self.assertEqual(message.role, Message.USER_ROLE)
        self.assertEqual(message.dialog, Message.TOOLS_DIALOG)
        self.assertEqual(message.content, "Hello")
        
    def test_construct_parts_missing_dialog(self):
        """Test parameter based constructor without a dialog"""
        message = Message(role=Message.SYSTEM_ROLE, content="Hello")
        self.assertEqual(message.role, Message.SYSTEM_ROLE)
        self.assertEqual(message.dialog, Message.GROUP_DIALOG)
        self.assertEqual(message.content, "Hello")
        
    def test_construct_parts_missing_content(self):
        """Test parameter based constructor without a content"""
        message = Message(role=Message.SYSTEM_ROLE, dialog=Message.TOOLS_DIALOG)
        self.assertEqual(message.role, Message.SYSTEM_ROLE)
        self.assertEqual(message.dialog, Message.TOOLS_DIALOG)
        self.assertEqual(message.content, "No Content String Provided")

    def test_as_LLM_Message(self):
        """Test the LLM Message projection """
        message = Message(role="assistant", dialog="group", content="How can I help")
        llm_message = {"role": "assistant", "content": "group:How can I help"}
        self.assertEqual(message.as_llm_message(), llm_message)
        
    def test_as_dict(self):
        """Test the LLM Message projection """
        message = Message(role="assistant", dialog="group", content="How can I help")
        message_dict = {"role": "assistant", "dialog":"group", "content": "How can I help"}
        self.assertEqual(message.as_dict(), message_dict)

if __name__ == "__main__":
    unittest.main()