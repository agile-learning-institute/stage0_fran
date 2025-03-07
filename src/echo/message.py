import logging
logger = logging.getLogger(__name__)

class Message:
    USER_ROLE = "user"
    ASSISTANT_ROLE = "assistant"
    SYSTEM_ROLE = "system"
    VALID_ROLES = [USER_ROLE, ASSISTANT_ROLE, SYSTEM_ROLE]
    GROUP_DIALOG = "group"
    TOOLS_DIALOG = "tools"
    INTERNAL_DIALOG = "you"
    VALID_DIALOGS = [GROUP_DIALOG, TOOLS_DIALOG, INTERNAL_DIALOG]
    
    def __init__(self, 
                 llm_message=None, ## Dict with role and content properties
                 encoded_text=None, ## String with From: To: structure
                 user="unknown", text="", 
                 role=USER_ROLE, dialog=GROUP_DIALOG):
        """
        Initialize a message, from a llm dict, 
        or encoded_text, or individual parameters.
        """
        self.user = user
        self.role = role
        self.dialog = dialog
        self.text = text
        
        # If an llm_message is provided use the role and parse the content
        if llm_message:
            self.role = llm_message["role"]
            self.user, self.dialog, self.text = self.decode(
                user=self.user, dialog=self.dialog, content=llm_message["content"])
        
        # If encoded text is provided, parse the content and take role (provided or default)
        elif encoded_text:
            self.user, self.dialog, self.text = self.decode(
                user=self.user, dialog=self.dialog, content=encoded_text)

    def decode(self, user=None, dialog=None, content=None):
        """Helper to decode from, to, text values from a content string"""
        try:
            parts = content.split(" ", 2)  # Split into 3 parts: 'From:<user>', 'To:<dialog>', and '<text>'
            user = parts[0].split("From:")[1]
            dialog = parts[1].split("To:")[1]
            text = parts[2] if len(parts) > 2 else ""
            if not dialog in self.VALID_DIALOGS: dialog=self.GROUP_DIALOG
            return user, dialog, text
        except (IndexError, ValueError):
            logger.debug(f"Raw message format used - content was \"{content[:40]}...\"")
            return user, dialog, content

    def as_llm_message(self):
        """Get a message with dialog added to the front of content."""
        return {
            "role": self.role,
            "content": f"From:{self.user} To:{self.dialog} {self.text}"
        }
            
    def as_dict(self):
        """Get a message as a plain dict for json serialization."""
        return {
            "role": self.role,
            "user": self.user,
            "dialog": self.dialog,
            "text": self.text
        }
