import json
import unittest
from unittest.mock import AsyncMock, patch, MagicMock
import discord
from echo.discord_bot import DiscordBot
from echo.echo import Echo
from echo.llm_handler import LLMHandler
from echo.agent import Agent

class TestDiscordBot(unittest.IsolatedAsyncioTestCase):
    
    async def asyncSetUp(self):
        """Set up the bot with mock dependencies before each test."""
        self.llm_handler = MagicMock(spec=LLMHandler)
        self.mock_agent = MagicMock(spec=Agent)  
        self.mock_agent.invoke_action = MagicMock()  
        
        self.bot = DiscordBot(self.mock_agent, "Test_Bot_ID", self.llm_handler)
        self.bot.active_channels = ["test-channel"]
        
        self.message = MagicMock()
        self.message.author.id = "USER-12345"
        self.message.author.username = "Alice"
        self.message.channel.id = "test-channel"
        self.message.channel.send = AsyncMock()
        self.message.mentions = [self.bot.user]
        self.message.channel.send = AsyncMock()
        self.message.content = ""
    
    async def test_on_message_first_dm(self):
        """Ensure DMs processed when unknown."""
        self.message.guild = None
        self.message.content = "Hello bot!"

        # Mock expected behavior
        mock_response = ["DM-USER-12345"]
        self.mock_agent.invoke_action.return_value = mock_response  # Directly mock return value
        self.llm_handler.handle_message.return_value = "Hello Alice!"
        
        await self.bot.on_message(self.message)

        # Ensure code worked as expected
        self.mock_agent.invoke_action.assert_called_once_with("add_channel", json.dumps({"bot_id": "Test_Bot_ID", "channel_id": "DM-USER-12345"}))
        self.assertEqual(self.message.channel.send.call_count, 2)
        self.message.channel.send.assert_any_call("✅ Channel: DM-USER-12345 added to active channels list.")
        self.message.channel.send.assert_any_call("Hello Alice!")

    async def test_on_message_second_dm(self):
        """Ensure DMs processed when known."""
        self.message.guild = None
        self.message.content = "Hello bot!"
        self.llm_handler.handle_message.return_value = "Hello Alice!"
        self.bot.active_channels = ["DM-USER-12345"]
        
        await self.bot.on_message(self.message)
        self.llm_handler.handle_message.assert_called_once_with(self.message.author.username, "DM-USER-12345", "Hello bot!")
        self.assertEqual(self.message.channel.send.call_count, 1)
        self.message.channel.send.assert_any_call("Hello Alice!")
    
    async def test_on_message_channel(self):
        """Respond to a known channel"""
        self.message.guild = "SERVER"
        self.message.content = "Hello bot!"
        self.llm_handler.handle_message.return_value = "Hello Alice!"
        self.bot.active_channels = ["test-channel"]
        
        await self.bot.on_message(self.message)
        self.llm_handler.handle_message.assert_called_once_with(self.message.author.username, "test-channel", "Hello bot!")
        self.assertEqual(self.message.channel.send.call_count, 1)
        self.message.channel.send.assert_any_call("Hello Alice!")
    
    @patch.object(DiscordBot, 'user', new_callable=MagicMock)
    async def test_on_message_leave(self, mock_user):
        """Ensure leave messages are processed."""
        # Set up mocks
        mock_user.username = "test-user"
        self.bot.user = mock_user
        self.message.content = "@test-user leave"
        self.message.mentions = [self.bot.user]
        self.mock_agent.invoke_action.return_value = []

        await self.bot.on_message(self.message)

        # Ensure bot_agent.invoke_action was called correctly
        self.mock_agent.invoke_action.assert_called_once_with("remove_channel", json.dumps({
            "bot_id": "Test_Bot_ID",
            "channel_id": "test-channel"
        }))

        # Ensure the bot sends the correct leave message
        self.message.channel.send.assert_called_once_with("✅ Channel: test-channel removed from active channels list.")
        self.assertEqual(self.message.channel.send.call_count, 1)
        
    @patch.object(DiscordBot, 'user', new_callable=MagicMock) 
    async def test_on_message_join(self, mock_user):
        """Ensure leave messages are processed."""
        mock_user.username = "test-user"
        self.bot.active_channels = []
        self.mock_agent.invoke_action.return_value = []
        self.message.content = "@test-user join"
        self.message.mentions = [self.bot.user]

        await self.bot.on_message(self.message)
        
        self.assertEqual(self.message.channel.send.call_count, 1)
        self.message.channel.send.assert_called_once_with("✅ Channel: test-channel added to active channels list.")
        
    @patch.object(discord.TextChannel, 'send', new_callable=AsyncMock)
    async def test_on_message_ignored_channel(self, mock_send):
        """Ensure messages in non-active channels are ignored."""
        self.message.channel.id = "random-channel"
        self.message.channel = MagicMock(spec=discord.TextChannel)
        self.message.channel.id = "test-unknown-channel-id"
        
        await self.bot.on_message(self.message)
        self.llm_handler.handle_message.assert_not_called()
        mock_send.assert_not_called()
    
if __name__ == "__main__":
    unittest.main()
