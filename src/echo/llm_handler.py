import json
import re
import logging
logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__name__)

class LLMHandler:
    """_summary_
    LLM handler implements the inner/outer chat discussions used by
    the Chat Engine. It persists the conversation using the 
    /conversation/add_message Agent Action
    """
    def __init__(self, handle_command_function=None, llm_client=None):
        """
        Initializes LLMHandler with an Echo agent framework and an LLM client.

        :param handle_command_function: Echo handle command function
        :param llm_client: Instance of LLMClient for LLM chat processing. (ollama_llm_client)
        """
        self.llm = llm_client
        self.handle_command = handle_command_function
        self.agent_command_pattern = re.compile(r"^/([^/]+)/([^/]+)(?:/(.*))?$")

    def handle_message(self, user=None, channel=None, message=None, dialog=None):
        """
        Processes an incoming message, using it to update the conversation, 
        and generate a reply. If the reply is on the "internal" dialog it will 
        process the message by invoking the requested agent/action. 

        :param user: The username of the sender.
        :param channel: The Discord channel where the message originated.
        :param message: The message content.
        :param dialog: The "internal" or "external" dialog this message will be posted to, defaults to external
        :return: The response to be written to the chat-channel. 
        """
        def post_message(from_role: str, to_role: str, content: str):
            """
            Small helper function to add a message to the conversation
            Uses the /conversation/add_message agent action
            
            :param from_role: Who is this message in the conversation "from" - system | agent | user
            :param to_role: Who is this message "to" - internal (agents) | external (chat)
            :param content: The message itself
            :return: The full conversation (list of messages)
            """
            formatted_message = {"from": from_role, "to": to_role, "content": content}
            arguments = json.dumps({"channel_id": channel, "message":formatted_message}, separators=(',', ':'))
            command_message = f"/conversation/add_message/{arguments}"
            logger.info(f"Sending Command Message: {command_message}")
            conversation = self.handle_command(command_message)
            return conversation if isinstance(conversation, list) else []

        # Set default dialog
        if not dialog: dialog = "external"
        
        # Step 1: Add the user message to the conversation
        logger.info(f"Posting Message {message}")
        messages = post_message(user, dialog, message)

        # Step 2: Check if this is an agent call using regex
        if self.agent_command_pattern.match(message):
            agent_reply = self.handle_command(message)
            logger.info(f"Command Message Sent: {message} reply: {agent_reply}")
            messages = post_message("agent", "internal", agent_reply)

        # Step 3: Call the LLM with updated conversation history
        logger.info(f"Getting Chat Reply")
        chat_reply = self.llm.chat(model=self.llm.model, messages=messages)
        logger.info(f"LLM Chat Reply {chat_reply}")

        # Step 4: Verify chat_reply conforms to template
        if not (isinstance(chat_reply, dict) and chat_reply["from"] and chat_reply["to"] and chat_reply["content"]):
            logger.warning(f"LLM Response is not formatted correctly {chat_reply}")
            chat_reply = {
                "from": "assistant",
                "to": "external",
                "content": chat_reply
            }

        # Step 5: Process LLM response recursively if it's an internal message
        if chat_reply["to"] == "internal":
            logger.info(f"Process LLM response recursively {chat_reply["content"]}")
            return self.handle_message(user="system", channel=channel, message=chat_reply["content"], dialog="internal")

        # Step 6: Add LLM response to conversation and return it
        logger.info(f"Posting LLM response message to chat: {chat_reply["content"]}")
        messages = post_message("system", "external", chat_reply["content"])
        return chat_reply["content"]

