import unittest
from unittest.mock import patch, MagicMock
from stage0_py_utils import Agent
from stage0_fran.agents.workshop_agent import create_workshop_agent

class TestWorkshopAgent(unittest.TestCase):
    
    def setUp(self):
        """Set up a mock bot agent."""
        self.mock_bot = Agent("test_bot_agent")
        self.mock_workshop = {}
        self.workshop_agent = create_workshop_agent(self.mock_bot)
        self.get_workshops = self.workshop_agent.actions["get_workshops"]["function"]
        self.get_workshop = self.workshop_agent.actions["get_workshop"]["function"]
        self.add_workshop = self.workshop_agent.actions["add_workshop"]["function"]
        self.update_workshop = self.workshop_agent.actions["update_workshop"]["function"]
        self.start_workshop = self.workshop_agent.actions["start_workshop"]["function"]
        self.advance_workshop = self.workshop_agent.actions["advance_workshop"]["function"]
        self.add_observation = self.workshop_agent.actions["add_observation"]["function"]

    @patch("stage0_fran.agents.workshop_agent.create_echo_token")  
    @patch("stage0_fran.agents.workshop_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.workshop_agent.WorkshopServices.get_workshops")
    def test_get_workshops_success(self, mock_get_workshops, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of get_workshops action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_get_workshops.return_value = "workshops_list"
        
        # Call function
        arguments = "^start"
        result = self.get_workshops(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_get_workshops.assert_called_once_with(query=arguments, token="fake_token")
        self.assertEqual(result, "workshops_list")
    
    @patch("stage0_fran.agents.workshop_agent.create_echo_token")  
    @patch("stage0_fran.agents.workshop_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.workshop_agent.WorkshopServices.get_workshops")
    def test_get_workshops_fail(self, mock_get_workshops, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test failure case for get_workshops action."""
        
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_get_workshops.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = "^start"
        result = self.get_workshops(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_get_workshops.assert_called_once_with(query=arguments, token="fake_token")
        self.assertEqual(result, "error")
        
    @patch("stage0_fran.agents.workshop_agent.create_echo_token")  
    @patch("stage0_fran.agents.workshop_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.workshop_agent.WorkshopServices.get_workshop")
    def test_get_workshop_success(self, mock_get_workshop, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of get_workshops action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_get_workshop.return_value = "a_workshop"
        
        # Call function
        arguments = "workshop_1"
        result = self.get_workshop(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_get_workshop.assert_called_once_with(workshop_id=arguments, token="fake_token")
        self.assertEqual(result, "a_workshop")
    
    @patch("stage0_fran.agents.workshop_agent.create_echo_token")  
    @patch("stage0_fran.agents.workshop_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.workshop_agent.WorkshopServices.get_workshop")
    def test_get_workshop_fail(self, mock_get_workshop, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test failure case for get_workshops action."""
        
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_get_workshop.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = "workshop_1"
        result = self.get_workshop(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_get_workshop.assert_called_once_with(workshop_id=arguments, token="fake_token")
        self.assertEqual(result, "error")
                
    @patch("stage0_fran.agents.workshop_agent.create_echo_token")  
    @patch("stage0_fran.agents.workshop_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.workshop_agent.WorkshopServices.update_workshop")
    def test_update_workshop_success(self, mock_update_workshop, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of update_workshop action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_update_workshop.return_value = "a_workshop"
        
        # Call function
        arguments = {
            "_id": "channel_1",
            "name": "workshop name"
        }
        result = self.update_workshop(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_update_workshop.assert_called_once_with(workshop_id=arguments["_id"], workshop=arguments, token="fake_token", breadcrumb="fake_breadcrumb")
        self.assertEqual(result, "a_workshop")
    
    @patch("stage0_fran.agents.workshop_agent.create_echo_token")  
    @patch("stage0_fran.agents.workshop_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.workshop_agent.WorkshopServices.update_workshop")
    def test_update_workshop_fail(self, mock_update_workshop, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of update_workshop action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_update_workshop.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = {
            "_id": "workshop_1",
            "name": "workshop name"
        }
        result = self.update_workshop(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_update_workshop.assert_called_once_with(workshop_id=arguments["_id"], workshop=arguments, token="fake_token", breadcrumb="fake_breadcrumb")
        self.assertEqual(result, "error")
                
    @patch("stage0_fran.agents.workshop_agent.create_echo_token")  
    @patch("stage0_fran.agents.workshop_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.workshop_agent.WorkshopServices.start_workshop")
    def test_start_workshop_success(self, mock_start_workshop, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of start_workshop action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_start_workshop.return_value = "a Workshop"
        
        # Call function
        arguments = "workshop_1"
        result = self.start_workshop(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_start_workshop.assert_called_once_with(workshop_id=arguments, token="fake_token", breadcrumb="fake_breadcrumb")
        self.assertEqual(result, "a Workshop")
    
    @patch("stage0_fran.agents.workshop_agent.create_echo_token")  
    @patch("stage0_fran.agents.workshop_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.workshop_agent.WorkshopServices.start_workshop")
    def test_start_workshop_fail(self, mock_start_workshop, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test failed execution of start_workshop action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_start_workshop.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = "workshop_1"
        result = self.start_workshop(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_start_workshop.assert_called_once_with(workshop_id=arguments, token="fake_token", breadcrumb="fake_breadcrumb")
        self.assertEqual(result, "error")
                            
    @patch("stage0_fran.agents.workshop_agent.create_echo_token")  
    @patch("stage0_fran.agents.workshop_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.workshop_agent.WorkshopServices.advance_workshop")
    def test_advance_workshop_success(self, mock_advance_workshop, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of advance_workshop action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_advance_workshop.return_value = "a Workshop"
        
        # Call function
        arguments = "workshop_1"
        result = self.advance_workshop(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_advance_workshop.assert_called_once_with(workshop_id=arguments, token="fake_token", breadcrumb="fake_breadcrumb")
        self.assertEqual(result, "a Workshop")
    
    @patch("stage0_fran.agents.workshop_agent.create_echo_token")  
    @patch("stage0_fran.agents.workshop_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.workshop_agent.WorkshopServices.advance_workshop")
    def test_advance_workshop_fail(self, mock_advance_workshop, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test failed execution of start_workshop action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_advance_workshop.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = "workshop_1"
        result = self.advance_workshop(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_advance_workshop.assert_called_once_with(workshop_id=arguments, token="fake_token", breadcrumb="fake_breadcrumb")
        self.assertEqual(result, "error")
                            
    @patch("stage0_fran.agents.workshop_agent.create_echo_token")  
    @patch("stage0_fran.agents.workshop_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.workshop_agent.WorkshopServices.add_observation")
    def test_add_observation_success(self, mock_add_observation, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of add_observation action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_add_observation.return_value = "a Workshop"
        
        # Call function
        arguments = {
            "workshop_id": "workshop_1",
            "observation": {"foo":"bar"}
        }
        result = self.add_observation(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_add_observation.assert_called_once_with(workshop_id=arguments["workshop_id"], observation=arguments["observation"], token="fake_token", breadcrumb="fake_breadcrumb")
        self.assertEqual(result, "a Workshop")
    
    @patch("stage0_fran.agents.workshop_agent.create_echo_token")  
    @patch("stage0_fran.agents.workshop_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.workshop_agent.WorkshopServices.add_observation")
    def test_add_observation_fail(self, mock_add_observation, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test failed execution of add_observation action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_add_observation.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = {
            "workshop_id": "workshop_1",
            "observation": {"foo":"bar"}
        }
        result = self.add_observation(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_add_observation.assert_called_once_with(workshop_id=arguments["workshop_id"], observation=arguments["observation"], token="fake_token", breadcrumb="fake_breadcrumb")
        self.assertEqual(result, "error")
                                
if __name__ == "__main__":
    unittest.main()
