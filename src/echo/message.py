import logging
logger = logging.getLogger(__name__)

class Message:
    USER_ROLE = "user"
    ASSISTANT_ROLE = "assistant"
    SYSTEM_ROLE = "system"
    VALID_ROLES = [USER_ROLE, ASSISTANT_ROLE, SYSTEM_ROLE]
    GROUP_DIALOG = "group"
    TOOLS_DIALOG = "tools"
    VALID_DIALOGS = [GROUP_DIALOG, TOOLS_DIALOG]
    
    def __init__(self, message=None, role=None, dialog=None, content=None):
        """Initialize a message."""
        if isinstance(message, str):
            # Construct default message from message
            self.role = Message.USER_ROLE
            self.dialog = Message.GROUP_DIALOG                
            self.content = message
            
        elif isinstance(message, dict):  
            # Construct from a message dict without a dialog property
            logger.info(f"Constructing from message {message}")
            self.role = message.get("role", Message.USER_ROLE)
            content_value = message.get("content", "")  

            # Ensure content is long enough before slicing
            if len(content_value) >= 6 and ":" in content_value[:6]:
                self.dialog, self.content = content_value.split(":", 1)
            else:
                self.dialog = Message.GROUP_DIALOG
                self.content = content_value  
        else:
            # Construct from individual parameters
            logger.info(f"Constructing from parameters {role}, {dialog}, {content}")
            if role in Message.VALID_ROLES:
                self.role = role
            else: 
                self.role = Message.USER_ROLE
                
            if dialog in Message.VALID_DIALOGS:
                self.dialog = dialog 
            else:
                self.dialog = Message.GROUP_DIALOG
                
            self.content = content or ""

    def as_llm_message(self):
        """Get a message with dialog added to the front of content."""
        return {
            "role": self.role,
            "content": f"{self.dialog}:{self.content}"
        }
            
    def as_dict(self):
        """Get a message as a plain dict for json serialization."""
        return {
            "role": self.role,
            "dialog": self.dialog,
            "content": self.content
        }
