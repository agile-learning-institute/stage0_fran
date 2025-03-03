import json
import re
from echo.message import Message
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

    def handle_message(self, channel=None, role=Message.USER_ROLE, dialog=None, text=None ):
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
        def post_message(role: str, dialog: str, content: str):
            """
            Small helper function to add a message to the conversation
            Uses the /conversation/add_message agent action
            
            :param from_role: Who is this message in the conversation "from" - system | agent | user
            :param to_role: Who is this message "to" - internal (agents) | external (chat)
            :param content: The message itself
            :return: The full conversation (list of messages)
            """
            message = Message(role=role, dialog=dialog, content=content)
            arguments = json.dumps({"channel_id": channel, "message":message.as_llm_message()}, separators=(',', ':'))
            command = f"/conversation/add_message/{arguments}"
            logger.debug(f"Sending the command: {command}")
            conversation = self.handle_command(command)
            return conversation if isinstance(conversation, list) else []

        # Set default dialog
        if not dialog: dialog = Message.GROUP_DIALOG
        if not role: role = Message.USER_ROLE
        
        # Step 1: Add the user message to the conversation
        logger.debug(f"Posting Message {text}")
        messages = post_message(role=role, dialog=dialog, content=text)

        # Step 2: Check if this is an agent call using regex
        if self.agent_command_pattern.match(text):
            agent_reply = self.handle_command(text)
            agent_reply_string = json.dumps(agent_reply, separators=(',', ':'))
            messages = post_message(role=Message.USER_ROLE, dialog=dialog, content=agent_reply_string)
            # If this was a direct user to agent call, return the reply to the group.
            if dialog == Message.GROUP_DIALOG: return agent_reply_string

        # Step 3: Call the LLM with updated conversation history
        llm_reply = self.llm.chat(model=self.llm.model, messages=messages)
        llm_role = llm_reply["message"]["role"]
        llm_content = llm_reply["message"]["content"]
        chat_reply = Message({"role": llm_role, "content": llm_content})
        logger.debug(f"LLM Reply: {llm_reply}, Role: {llm_role}, Content: {llm_content}")

        # Step 4: Process LLM response recursively if it's an tool message
        if chat_reply.dialog == Message.TOOLS_DIALOG:
            logger.debug(f"Process LLM response recursively {chat_reply.content}")
            return self.handle_message(channel=channel, role=chat_reply.role, text=chat_reply.content, dialog=chat_reply.dialog)

        # Step 6: Add LLM response to conversation and return it
        logger.debug(f"Posting LLM response message to chat: {chat_reply.content}")
        post_message(role=chat_reply.role, dialog=chat_reply.dialog, content=chat_reply.content)
        return chat_reply.content

