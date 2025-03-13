import unittest
from unittest.mock import patch, MagicMock
from stage0_py_utils import Agent
from stage0_fran.agents.chain_agent import create_chain_agent

class TestChainAgent(unittest.TestCase):
    
    def setUp(self):
        """Set up a mock bot agent."""
        self.mock_bot = Agent("mock bot")
        chain_agent = create_chain_agent(self.mock_bot)
        self.get_chains = chain_agent.actions["get_chains"]["function"]
        self.get_chain = chain_agent.actions["get_chain"]["function"]

    @patch("stage0_fran.agents.chain_agent.create_echo_token")  
    @patch("stage0_fran.agents.chain_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.chain_agent.ChainServices.get_chains")
    def test_get_chains_success(self, mock_get_chains, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of get_chains action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_get_chains.return_value = "chains_list"
        
        # Call function
        arguments = ""
        result = self.get_chains(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_get_chains.assert_called_once_with(token="fake_token")
        self.assertEqual(result, "chains_list")
    
    @patch("stage0_fran.agents.chain_agent.create_echo_token")  
    @patch("stage0_fran.agents.chain_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.chain_agent.ChainServices.get_chains")
    def test_get_chains_fail(self, mock_get_chains, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test failure case for get_chains action."""
        
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_get_chains.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = ""
        result = self.get_chains(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_get_chains.assert_called_once_with(token="fake_token")
        self.assertEqual(result, "error")
                    
    @patch("stage0_fran.agents.chain_agent.create_echo_token")  
    @patch("stage0_fran.agents.chain_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.chain_agent.ChainServices.get_chain")
    def test_get_chain_success(self, mock_get_chain, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of get_chains action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_get_chain.return_value = "a_chain"
        
        # Call function
        arguments = "A_CHAIN_ID"
        result = self.get_chain(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_get_chain.assert_called_once_with(chain_id=arguments, token="fake_token")
        self.assertEqual(result, "a_chain")
    
    @patch("stage0_fran.agents.chain_agent.create_echo_token")  
    @patch("stage0_fran.agents.chain_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.chain_agent.ChainServices.get_chain")
    def test_get_chain_fail(self, mock_get_chain, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test failure case for get_chains action."""
        
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_get_chain.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = "CHAIN_ID"
        result = self.get_chain(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_get_chain.assert_called_once_with(chain_id=arguments, token="fake_token")
        self.assertEqual(result, "error")
                    
if __name__ == "__main__":
    unittest.main()
