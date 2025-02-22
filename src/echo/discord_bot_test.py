import unittest
from unittest.mock import AsyncMock, patch, MagicMock
import discord
from echo.discord_bot import DiscordBot
from echo.echo import Echo
from echo.llm_handler import LLMHandler

class TestDiscordBot(unittest.IsolatedAsyncioTestCase):
    
    async def asyncSetUp(self):
        """Set up the bot with mock dependencies before each test."""
        self.echo = MagicMock(spec=Echo)
        self.llm_handler = MagicMock(spec=LLMHandler)
        self.intents = discord.Intents.default()
        self.bot = DiscordBot(self.echo, self.llm_handler, intents=self.intents)
        self.bot.active_channels = ["test-channel"]
    
    async def test_on_message_first_dm(self):
        """Ensure DMs processed when unknown."""
        message = MagicMock()
        message.guild = None
        message.author.id = "USER-12345"
        message.author.username = "Alice"
        message.content = "Hello bot!"
        message.channel.send = AsyncMock()
        self.llm_handler.handle_message.return_value = "Hello Alice!"
        self.echo.handle_command.return_value = ["DM-USER-12345"]
        
        await self.bot.on_message(message)
        self.llm_handler.handle_message.assert_called_once_with(message.author.username, "DM-USER-12345", "Hello bot!")
        self.assertEqual(message.channel.send.call_count, 2)
        message.channel.send.assert_any_call("✅ Channel: DM-USER-12345 added to active channels list.")
        message.channel.send.assert_any_call("Hello Alice!")

    async def test_on_message_second_dm(self):
        """Ensure DMs processed when known."""
        message = MagicMock()
        message.guild = None
        message.author.id = "USER-12345"
        message.author.username = "Alice"
        message.content = "Hello bot!"
        message.channel.send = AsyncMock()
        self.llm_handler.handle_message.return_value = "Hello Alice!"
        self.bot.active_channels = ["DM-USER-12345"]
        
        await self.bot.on_message(message)
        self.llm_handler.handle_message.assert_called_once_with(message.author.username, "DM-USER-12345", "Hello bot!")
        self.assertEqual(message.channel.send.call_count, 1)
        message.channel.send.assert_any_call("Hello Alice!")
    
    async def test_on_message_channel(self):
        """Respond to a known channel"""
        message = MagicMock()
        message.guild = "SERVER"
        message.author.id = "USER-12345"
        message.author.username = "Alice"
        message.channel.id = "test-channel"
        message.content = "Hello bot!"
        message.channel.send = AsyncMock()
        self.llm_handler.handle_message.return_value = "Hello Alice!"
        self.bot.active_channels = ["test-channel"]
        
        await self.bot.on_message(message)
        self.llm_handler.handle_message.assert_called_once_with(message.author.username, "test-channel", "Hello bot!")
        self.assertEqual(message.channel.send.call_count, 1)
        message.channel.send.assert_any_call("Hello Alice!")
    
    @patch.object(DiscordBot, 'user', new_callable=MagicMock) 
    async def test_on_message_leave(self, mock_user):
        """Ensure leave messages are processed."""
        mock_user.username = "test-user"
        self.bot.user = MagicMock()
        self.bot.user.username = "test-user"                
        self.bot.active_channels = ["test-channel"]
        self.echo.handle_command.return_value = []
            
        message = MagicMock()
        message.guild = "SERVER"
        message.author.id = "USER-12345"
        message.author.username = "Alice"
        message.channel.id = "test-channel"
        message.content = "@test-user leave"
        message.mentions = [self.bot.user]
        message.channel.send = AsyncMock()

        await self.bot.on_message(message)
        self.assertEqual(message.channel.send.call_count, 1)
        message.channel.send.assert_called_once_with("✅ Channel: test-channel removed from active channels list.")
        
    @patch.object(DiscordBot, 'user', new_callable=MagicMock) 
    async def test_on_message_join(self, mock_user):
        """Ensure leave messages are processed."""
        mock_user.username = "test-user"
        self.bot.user = MagicMock()
        self.bot.user.username = "test-user"                
        self.bot.active_channels = []
        self.echo.handle_command.return_value = ["test-channel"]
            
        message = MagicMock()
        message.guild = "SERVER"
        message.author.id = "USER-12345"
        message.author.username = "Alice"
        message.channel.id = "test-channel"
        message.content = "@test-user join"
        message.mentions = [self.bot.user]
        message.channel.send = AsyncMock()

        await self.bot.on_message(message)
        self.assertEqual(message.channel.send.call_count, 1)
        message.channel.send.assert_called_once_with("✅ Channel: test-channel added to active channels list.")
        
    @patch.object(discord.TextChannel, 'send', new_callable=AsyncMock)
    async def test_on_message_ignored_channel(self, mock_send):
        """Ensure messages in non-active channels are ignored."""
        message = MagicMock()
        message.author.username = "Charlie"
        message.content = "Hello?"
        message.channel.id = "random-channel"
        message.channel = MagicMock(spec=discord.TextChannel)
        message.channel.id = "test-channel-id"
        message.author = MagicMock()
        
        await self.bot.on_message(message)
        self.llm_handler.handle_message.assert_not_called()
        mock_send.assert_not_called()
    
if __name__ == "__main__":
    unittest.main()
