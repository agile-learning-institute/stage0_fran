import json
from echo import Echo

class LLMHandler:
    def __init__(self, echo_framework):
        self.echo = echo_framework

    async def handle_message(self, message):
        """
        Processes incoming messages, determines whether to respond as LLM,
        call an agent, or forward a response.
        """
        structured_message = self.parse_message_format(message.content)
        
        if not structured_message:
            return "Invalid message format. Use FROM: TO: MESSAGE:"

        from_user = structured_message["FROM"]
        to_user = structured_message["TO"]
        msg_content = structured_message["MESSAGE"]

        if to_user == "GROUP":
            return await self.handle_group_message(from_user, msg_content)

        elif to_user == "AGENT":
            return await self.call_agent(msg_content)

        elif to_user == "LLM":
            return await self.handle_llm_message(from_user, msg_content)

        return "Unknown recipient."

    async def handle_group_message(self, from_user, msg_content):
        """
        Handles messages sent to the GROUP.
        - If it's a command, the LLM might translate it to an agent request.
        - Otherwise, it engages in conversation.
        """
        if msg_content.startswith("/"):
            # Assume user is trying to call an agent
            return await self.call_agent(msg_content)

        # Otherwise, LLM processes it as a general chat message
        return f"{from_user} said: {msg_content}"

    async def call_agent(self, agent_command):
        """
        Extracts agent/action/arguments and calls Echo to execute it.
        """
        match = self.parse_command(agent_command)
        if not match:
            return "Invalid agent command format."

        agent, action, arguments = match
        response = await self.echo.handle_command(agent, action, arguments, None, None)

        # Return in structured format
        return f"FROM: AGENT\nTO: LLM\nMESSAGE: {response}"

    async def handle_llm_message(self, from_user, msg_content):
        """
        The LLM generates a response to a user or system message.
        """
        return f"FROM: LLM\nTO: GROUP\nMESSAGE: {self.llm_generate_response(from_user, msg_content)}"

    def parse_message_format(self, message_text):
        """
        Parses a structured message in the FROM: TO: MESSAGE: format.
        Returns a dictionary or None if invalid.
        """
        try:
            lines = message_text.split("\n")
            if len(lines) < 3:
                return None  # Invalid format

            from_user = lines[0].split(": ", 1)[1]
            to_user = lines[1].split(": ", 1)[1]
            msg_content = lines[2].split(": ", 1)[1]

            return {"FROM": from_user, "TO": to_user, "MESSAGE": msg_content}

        except (IndexError, ValueError):
            return None  # Parsing failed

    def parse_command(self, message_content):
        """
        Parses an /agent/action/arguments command.
        Returns (agent, action, arguments) or None if invalid.
        """
        import re
        match = re.match(r"^/(\w+)/(\w+)/(.*)", message_content)
        if not match:
            return None

        agent, action, arguments_str = match.groups()
        try:
            arguments = json.loads(arguments_str) if arguments_str else None
        except json.JSONDecodeError:
            arguments = None  # Invalid JSON, pass None

        return agent, action, arguments

    def llm_generate_response(self, from_user, msg_content):
        """
        Placeholder for LLM-generated responses.
        Replace with actual model call.
        """
        return f"I understand, {from_user}. Let me check that for you."