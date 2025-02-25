import unittest
from unittest.mock import patch, MagicMock
from echo.agent import Agent
from agents.bot_agent import create_bot_agent

class TestBotAgent(unittest.TestCase):
    
    def setUp(self):
        """Set up a mock bot agent."""
        self.mock_bot = Agent("test_bot_agent")
        bot_agent = create_bot_agent(self.mock_bot)
        self.get_bot = bot_agent.actions["get_bot"]["function"]
        self.get_channels = bot_agent.actions["get_channels"]["function"]
        self.add_channel = bot_agent.actions["add_channel"]["function"]
        self.remove_channel = bot_agent.actions["remove_channel"]["function"]

    @patch("agents.bot_agent.create_token")  
    @patch("agents.bot_agent.BotServices.get_bot")
    def test_get_bot_success(self, mock_get_bot, mock_create_token):
        """Test successful execution of get_bot action."""
        mock_bot_object = {
            "_id": "12345",
            "status": "active",
            "name": "TestBot",
            "description": "A test bot",
            "channels": ["channel_1", "channel_2"],
            "last_saved": "breadcrumb_data"
        }
        
        # Mock return values
        mock_create_token.return_value = "fake_token"
        mock_get_bot.return_value = mock_bot_object
        
        # Call function
        arguments = "test_bot_id"
        result = self.get_bot(arguments)
        
        # Assertions
        mock_create_token.assert_called_once()
        mock_get_bot.assert_called_once_with(arguments, "fake_token")
        self.assertEqual(result, mock_bot_object)
    
    @patch("agents.bot_agent.create_token")  
    @patch("agents.bot_agent.BotServices.get_bot")
    def test_get_bot_fail(self, mock_get_bot, mock_create_token):
        """Test failure case for get_bot action."""
        
        # Mock return values
        mock_create_token.return_value = "fake_token"
        mock_get_bot.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = {"description": "test_bot_id"}
        result = self.get_bot(arguments)
        
        # Assertions
        mock_create_token.assert_called_once()
        mock_get_bot.assert_called_once_with(arguments, "fake_token")
        self.assertEqual(result, "error")
        
    @patch("agents.bot_agent.create_token")  
    @patch("agents.bot_agent.BotServices.get_channels")
    def test_get_channels_success(self, mock_get_channels, mock_create_token):
        """Test successful execution of get_bot action."""
        mock_channels = ["channel_1", "channel_2"]
        
        # Mock return values
        mock_create_token.return_value = "fake_token"
        mock_get_channels.return_value = mock_channels
        
        # Call function
        arguments = "test_bot_id"
        result = self.get_channels(arguments)
        
        # Assertions
        mock_create_token.assert_called_once()
        mock_get_channels.assert_called_once_with(arguments, "fake_token")
        self.assertEqual(result, mock_channels)
    
    @patch("agents.bot_agent.create_token")  
    @patch("agents.bot_agent.BotServices.get_channels")
    def test_get_channels_fail(self, mock_get_channels, mock_create_token):
        """Test failure case for get_bot action."""
        
        # Mock return values
        mock_create_token.return_value = "fake_token"
        mock_get_channels.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = {"description": "test_bot_id"}
        result = self.get_channels(arguments)
        
        # Assertions
        mock_create_token.assert_called_once()
        mock_get_channels.assert_called_once_with(arguments, "fake_token")
        self.assertEqual(result, "error")
        
    @patch("agents.bot_agent.create_token")  
    @patch("agents.bot_agent.create_breadcrumb")  
    @patch("agents.bot_agent.BotServices.add_channel")
    def test_add_channel_success(self, mock_add_channel, mock_create_breadcrumb, mock_create_token):
        """Test successful execution of get_bot action."""
        mock_channels = ["channel_1", "channel_2"]
        
        # Mock return values
        mock_create_token.return_value = "fake_token"
        mock_create_breadcrumb.return_value = "fake_breadcrumb"
        mock_add_channel.return_value = mock_channels
        
        # Call function
        arguments = {
            "bot_id":"test_bot_id",
            "channel_id":"test_channel"
        }
        result = self.add_channel(arguments)
        
        # Assertions
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with("fake_token")
        mock_add_channel.assert_called_once_with("test_bot_id", "test_channel", "fake_token", "fake_breadcrumb")
        self.assertEqual(result, mock_channels)
    
    @patch("agents.bot_agent.create_token")  
    @patch("agents.bot_agent.create_breadcrumb")  
    @patch("agents.bot_agent.BotServices.add_channel")
    def test_add_channel_fail(self, mock_add_channel, mock_create_breadcrumb, mock_create_token):
        """Test failure case for get_bot action."""
        
        # Mock return values
        mock_create_token.return_value = "fake_token"
        mock_create_breadcrumb.return_value = "fake_breadcrumb"
        mock_add_channel.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = {
            "bot_id":"test_bot_id",
            "channel_id":"test_channel"
        }
        result = self.add_channel(arguments)
        
        # Assertions
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with("fake_token")
        mock_add_channel.assert_called_once_with(arguments["bot_id"], arguments["channel_id"], "fake_token", "fake_breadcrumb")
        self.assertEqual(result, "error")
        
    @patch("agents.bot_agent.create_token")  
    @patch("agents.bot_agent.create_breadcrumb")  
    @patch("agents.bot_agent.BotServices.remove_channel")
    def test_remove_channel_success(self, mock_remove_channel, mock_create_breadcrumb, mock_create_token):
        """Test successful execution of get_bot action."""
        mock_channels = ["channel_1", "channel_2"]
        
        # Mock return values
        mock_create_token.return_value = "fake_token"
        mock_create_breadcrumb.return_value = "fake_breadcrumb"
        mock_remove_channel.return_value = mock_channels
        
        # Call function
        arguments = {
            "bot_id":"test_bot_id",
            "channel_id":"test_channel"
        }
        result = self.remove_channel(arguments)
        
        # Assertions
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with("fake_token")
        mock_remove_channel.assert_called_once_with("test_bot_id", "test_channel", "fake_token", "fake_breadcrumb")
        self.assertEqual(result, mock_channels)
    
    @patch("agents.bot_agent.create_token")  
    @patch("agents.bot_agent.create_breadcrumb")  
    @patch("agents.bot_agent.BotServices.remove_channel")
    def test_remove_channel_fail(self, mock_remove_channel, mock_create_breadcrumb, mock_create_token):
        """Test failure case for get_bot action."""
        
        # Mock return values
        mock_create_token.return_value = "fake_token"
        mock_create_breadcrumb.return_value = "fake_breadcrumb"
        mock_remove_channel.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = {
            "bot_id":"test_bot_id",
            "channel_id":"test_channel"
        }
        result = self.remove_channel(arguments)
        
        # Assertions
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with("fake_token")
        mock_remove_channel.assert_called_once_with(arguments["bot_id"], arguments["channel_id"], "fake_token", "fake_breadcrumb")
        self.assertEqual(result, "error")
        
if __name__ == "__main__":
    unittest.main()
