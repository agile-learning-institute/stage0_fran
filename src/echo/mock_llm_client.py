
import random


class MockLLMClient:
    """_summary_
    Mock Client for Testing 
    """
    def __init__(self, base_url=None, model=None):
        """
        Initializes the LLMClient list of possible replies
        """
        self.model = model
        self.base_url = base_url
        self.replies = [
            {"message": {"role": "assistant", "content": "group:Scant seconds later I hear the boss's phone ringing. I'll give the boss"}},
            {"message": {"role": "assistant", "content": "group:about 10 minutes of irate assistants, then wander round and suggest the"}},
            {"message": {"role": "assistant", "content": "group:helpdesk staff need a lesson on what's funny and what's not. Forwarding"}},
            {"message": {"role": "assistant", "content": "group:your phone to the boss at network failure ISN'T funny. Helpdesk personnel"}},
            {"message": {"role": "assistant", "content": "group:However, if as I surmise this is a thinly disguised ploy by the "}},
            {"message": {"role": "assistant", "content": "group:departmental Brown-Nose to edge his way one rung up the perk ladder into a "}},
            {"message": {"role": "assistant", "content": "group:trip to look at new security software, then I believe that our exposure to "}},
            {"message": {"role": "assistant", "content": "group:danger is somewhat overstated."}}
         ]

    def chat(self, model: str, messages: list):
        """
        Get a random reply
        """
        return random.choice(self.replies)
