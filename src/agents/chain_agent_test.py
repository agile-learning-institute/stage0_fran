import unittest
from unittest.mock import patch, MagicMock
from echo.agent import Agent
from agents.chain_agent import create_chain_agent

class TestChainAgent(unittest.TestCase):
    
    def setUp(self):
        """Set up a mock bot agent."""
        self.mock_bot = Agent("test_bot_agent")
        self.mock_chain = {}
        create_chain_agent(self.mock_bot)
        self.get_chains = self.mock_bot.actions["get_chains"]["function"]
        self.get_chain = self.mock_bot.actions["get_chain"]["function"]

    @patch("agents.chain_agent.create_token")  
    @patch("agents.chain_agent.create_breadcrumb")  
    @patch("agents.chain_agent.ChainServices.get_chains")
    def test_get_chains_success(self, mock_get_chains, mock_create_breadcrumb, mock_create_token):
        """Test successful execution of get_chains action."""
       
        # Mock return values
        mock_create_token.return_value = "fake_token"
        mock_create_breadcrumb.return_value = "fake_breadcrumb"
        mock_get_chains.return_value = "chains_list"
        
        # Call function
        arguments = ""
        result = self.get_chains(arguments)
        
        # Assertions
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with("fake_token")
        mock_get_chains.assert_called_once_with(token="fake_token")
        self.assertEqual(result, "chains_list")
    
    @patch("agents.chain_agent.create_token")  
    @patch("agents.chain_agent.create_breadcrumb")  
    @patch("agents.chain_agent.ChainServices.get_chains")
    def test_get_chains_fail(self, mock_get_chains, mock_create_breadcrumb, mock_create_token):
        """Test failure case for get_chains action."""
        
        # Mock return values
        mock_create_token.return_value = "fake_token"
        mock_create_breadcrumb.return_value = "fake_breadcrumb"
        mock_get_chains.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = ""
        result = self.get_chains(arguments)
        
        # Assertions
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with("fake_token")
        mock_get_chains.assert_called_once_with(token="fake_token")
        self.assertEqual(result, "error")
                    
    @patch("agents.chain_agent.create_token")  
    @patch("agents.chain_agent.create_breadcrumb")  
    @patch("agents.chain_agent.ChainServices.get_chain")
    def test_get_chain_success(self, mock_get_chain, mock_create_breadcrumb, mock_create_token):
        """Test successful execution of get_chains action."""
       
        # Mock return values
        mock_create_token.return_value = "fake_token"
        mock_create_breadcrumb.return_value = "fake_breadcrumb"
        mock_get_chain.return_value = "a_chain"
        
        # Call function
        arguments = "A_CHAIN_ID"
        result = self.get_chain(arguments)
        
        # Assertions
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with("fake_token")
        mock_get_chain.assert_called_once_with(chain_id=arguments, token="fake_token")
        self.assertEqual(result, "a_chain")
    
    @patch("agents.chain_agent.create_token")  
    @patch("agents.chain_agent.create_breadcrumb")  
    @patch("agents.chain_agent.ChainServices.get_chain")
    def test_get_chain_fail(self, mock_get_chain, mock_create_breadcrumb, mock_create_token):
        """Test failure case for get_chains action."""
        
        # Mock return values
        mock_create_token.return_value = "fake_token"
        mock_create_breadcrumb.return_value = "fake_breadcrumb"
        mock_get_chain.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = "CHAIN_ID"
        result = self.get_chain(arguments)
        
        # Assertions
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with("fake_token")
        mock_get_chain.assert_called_once_with(chain_id=arguments, token="fake_token")
        self.assertEqual(result, "error")
                    
if __name__ == "__main__":
    unittest.main()
