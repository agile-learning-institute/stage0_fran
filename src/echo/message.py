import logging
logger = logging.getLogger(__name__)

class Message:
    USER_ROLE = "user"
    ASSISTANT_ROLE = "assistant"
    SYSTEM_ROLE = "system"
    GROUP_DIALOG = "group"
    TOOLS_DIALOG = "tools"
    
    def __init__(self, role=None, dialog=None, content=None, message=None):
        """Initialize a message."""
        if message:
            # parse and remove dialog from message:content
            self.role = message["role"]
            self.dialog = message["content"][0:5]
            self.content = message["content"][6:]
            return
        else:
            self.role = role or Message.USER_ROLE
            self.dialog = dialog or Message.GROUP_DIALOG
            self.content = content or ""

    def get_llm_message(self):
        """Get a message with dialog added to the front of content."""
        return {
            "role": self.role,
            "content": f"{self.dialog}:{self.content}"
        }
