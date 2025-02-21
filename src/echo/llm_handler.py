import re
from echo.ollama_llm_client import OllamaLLMClient
from echo.echo import Echo

class LLMHandler:
    def __init__(self, echo_framework, llm_client):
        """
        Initializes LLMHandler with an Echo agent framework and an LLM client.

        :param echo_framework: Instance of Echo to route agent calls.
        :param llm_client: Instance of OllamaLLMClient for LLM chat processing.
        """
        self.echo = echo_framework
        self.llm = llm_client
        self.agent_command_pattern = re.compile(r"^/([^/]+)/([^/]+)(?:/(.*))?$")

    def handle_message(self, user: str, channel: str, message: str):
        """
        Processes an incoming message, determines if it's an agent call,
        updates the conversation, and invokes the LLM for a response.

        :param user: The username of the sender.
        :param channel: The Discord channel where the message originated.
        :param message: The message content.
        :return: The LLM-generated response.
        """
        # Step 1: Add the user message to the conversation
        messages = self.post_message(user, "external", message)

        # Step 2: Check if this is an agent call using regex
        if self.agent_command_pattern.match(message):
            agent_reply = self.echo.handle_command(message)
            messages = self.post_message("agent", "internal", agent_reply)

        # Step 3: Call the LLM with updated conversation history
        chat_reply = self.llm.chat(model=self.llm.model, messages=messages)

        # Step 4: Process LLM response recursively if it's an internal message
        if isinstance(chat_reply, dict) and chat_reply.get("to") == "internal":
            return self.handle_message("system", channel, chat_reply["content"])

        # Step 5: Add LLM response to conversation and return it
        messages = self.post_message("system", "external", chat_reply)

        return chat_reply

    def post_message(self, from_role: str, to_role: str, content: str):
        """
        Posts a message to the conversation and returns the updated messages list.

        :param from_role: Sender of the message (e.g., user, agent, system).
        :param to_role: Recipient of the message (e.g., external, internal).
        :param content: Message content.
        :return: Updated conversation message list.
        """
        formatted_message = [{"from": from_role, "to": to_role, "content": content}]
        conversation = self.echo.handle_command(f"/conversation/add_message/{formatted_message}")
        return conversation if isinstance(conversation, list) else []