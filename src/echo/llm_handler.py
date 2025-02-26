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

        :param echo_framework: Instance of Echo to route agent calls.
        :param llm_client: Instance of LLMClient for LLM chat processing. (ollama_llm_client)
        """
        self.llm = llm_client
        self.handle_command = handle_command_function
        self.agent_command_pattern = re.compile(r"^/([^/]+)/([^/]+)(?:/(.*))?$")

    def handle_message(self, user: str, channel: str, message: str):
        """
        Processes an incoming message, using it to update the conversation, 
        and generate a reply. If the reply is on the "internal" dialog it will 
        process the message by invoking the requested agent/action. 

        :param user: The username of the sender.
        :param channel: The Discord channel where the message originated.
        :param message: The message content.
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
            formatted_message = json.dumps({"from": from_role, "to": to_role, "content": content}, separators=(',', ':'))
            conversation = self.handle_command(f"/conversation/add_message/{formatted_message}")
            return conversation if isinstance(conversation, list) else []

        # Step 1: Add the user message to the conversation
        logger.debug(f"Posting Message {message}")
        messages = post_message(user, "external", message)

        # Step 2: Check if this is an agent call using regex
        if self.agent_command_pattern.match(message):
            logger.debug(f"Calling agent")
            agent_reply = self.handle_command(message)
            messages = post_message("agent", "internal", agent_reply)

        # Step 3: Call the LLM with updated conversation history
        logger.debug(f"Calling llm chat")
        chat_reply = self.llm.chat(model=self.llm.model, messages=messages)

        # Step 4: Process LLM response recursively if it's an internal message
        if isinstance(chat_reply, dict) and chat_reply.get("to") == "internal":
            logger.debug(f"Process LLM response recursively")
            return self.handle_message("system", channel, chat_reply["content"])

        # Step 5: Add LLM response to conversation and return it
        messages = post_message("system", "external", chat_reply)
        logger.debug(f"Posting LLM response message")

        return chat_reply
