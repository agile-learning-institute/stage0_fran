import unittest
from unittest.mock import patch, MagicMock
from echo.agent import Agent
from agents.echo_agent import create_echo_agent
from agents.config_agent import create_config_agent

class TestEchoAgent(unittest.TestCase):
    
    def setUp(self):
        """Set up a mock bot agent."""
        self.mock_agents = {"foo":"bar"}
        self.mock_bot = Agent("test_bot_agent")
        self.echo_agent = create_echo_agent(self.mock_bot, self.mock_agents)
        self.get_agents = self.echo_agent.actions["get_agents"]["function"]

    @patch("agents.echo_agent.create_token")  
    @patch("agents.echo_agent.create_breadcrumb")  
    def test_get_agents_success(self, mock_create_breadcrumb, mock_create_token):
        """Test successful execution of get_agents action."""
       
        # Mock return values
        mock_create_token.return_value = "fake_token"
        mock_create_breadcrumb.return_value = "fake_breadcrumb"
        
        # Call function
        arguments = ""
        result = self.get_agents(arguments)
        
        # Assertions
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with("fake_token")
        self.assertEqual(result, self.mock_agents)
                    
if __name__ == "__main__":
    unittest.main()
