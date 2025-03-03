
import random


class MockLLMClient:
    """_summary_
    Mock Client for Testing 
    """
    def __init__(self):
        """
        Initializes the LLMClient list of possible replies
        """
        self.replies = [
            "group:Scant seconds later I hear the boss's phone ringing. I'll give the boss",
            "group:about 10 minutes of irate users, then wander round and suggest the",
            "group:helpdesk staff need a lesson on what's funny and what's not. Forwarding",
            "group:your phone to the boss at network failure ISN'T funny. Helpdesk personnel",
            "group:However, if as I surmise this is a thinly disguised ploy by the ",
            "group:departmental Brown-Nose to edge his way one rung up the perk ladder into a ",
            "group:trip to look at new security software, then I believe that our exposure to ",
            "group:danger is somewhat overstated."
         ]

    def chat(self, model: str, messages: list):
        """
        Get a random reply
        """
        return random.choice(self.replies)
