import unittest
from unittest.mock import patch, MagicMock
from stage0_py_utils import Agent
from stage0_fran.agents.exercise_agent import create_exercise_agent

class TestExerciseAgent(unittest.TestCase):
    
    def setUp(self):
        """Set up a mock bot agent."""
        self.mock_exercise = {}
        self.mock_bot = Agent("test_bot_agent")
        self.exercise_agent = create_exercise_agent(self.mock_bot)
        self.get_exercises = self.exercise_agent.actions["get_exercises"]["function"]
        self.get_exercise = self.exercise_agent.actions["get_exercise"]["function"]

    @patch("stage0_fran.agents.exercise_agent.create_echo_token")  
    @patch("stage0_fran.agents.exercise_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.exercise_agent.ExerciseServices.get_exercises")
    def test_get_exercises_success(self, mock_get_exercises, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of get_exercises action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_get_exercises.return_value = "exercises_list"
        
        # Call function
        arguments = ""
        result = self.get_exercises(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_get_exercises.assert_called_once_with(token="fake_token")
        self.assertEqual(result, "exercises_list")
    
    @patch("stage0_fran.agents.exercise_agent.create_echo_token")  
    @patch("stage0_fran.agents.exercise_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.exercise_agent.ExerciseServices.get_exercises")
    def test_get_exercises_fail(self, mock_get_exercises, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test failure case for get_exercises action."""
        
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_get_exercises.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = ""
        result = self.get_exercises(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_get_exercises.assert_called_once_with(token="fake_token")
        self.assertEqual(result, "error")
                    
    @patch("stage0_fran.agents.exercise_agent.create_echo_token")  
    @patch("stage0_fran.agents.exercise_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.exercise_agent.ExerciseServices.get_exercise")
    def test_get_exercise_success(self, mock_get_exercise, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of get_exercises action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_get_exercise.return_value = "a_exercise"
        
        # Call function
        arguments = "A_CHAIN_ID"
        result = self.get_exercise(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_get_exercise.assert_called_once_with(exercise_id=arguments, token="fake_token")
        self.assertEqual(result, "a_exercise")
    
    @patch("stage0_fran.agents.exercise_agent.create_echo_token")  
    @patch("stage0_fran.agents.exercise_agent.create_echo_breadcrumb")  
    @patch("stage0_fran.agents.exercise_agent.ExerciseServices.get_exercise")
    def test_get_exercise_fail(self, mock_get_exercise, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test failure case for get_exercises action."""
        
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        mock_get_exercise.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = "CHAIN_ID"
        result = self.get_exercise(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_get_exercise.assert_called_once_with(exercise_id=arguments, token="fake_token")
        self.assertEqual(result, "error")
                    
if __name__ == "__main__":
    unittest.main()
