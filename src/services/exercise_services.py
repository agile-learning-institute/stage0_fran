from src.config.config import Config
import logging

from src.mongo_utils.mongo_io import MongoIO
logger = logging.getLogger(__name__)

class ExerciseServices:

    @staticmethod 
    def _check_user_access(token):
        """Role Based Access Control logic"""
        return # No RBAC yet

    @staticmethod
    def get_exercises(token):
        """Get a list of chains that match query"""
        ExerciseServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        match = None
        project = {"_id":1, "name":1}
        exercises = mongo.get_documents(config.EXERCISE_COLLECTION_NAME, match, project)
        return exercises

    @staticmethod
    def get_exercise(exercise_id, token):
        """Get the specified exercise"""
        ExerciseServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        exercise = mongo.get_document(config.EXERCISE_COLLECTION_NAME, exercise_id)
        return exercise
    
exercises = [
    {
        "exercise_name":"stakeholders",
        "purpose": "",
        "exercise_introduction": "What is this exercise",
        "observe_instructions":"How to observe as a Chat User",
        "observation_schema": {
            "description": "",
            "type": "object",
            "properties": {
                "name": {
                    "description": "",
                    "type": "sentence"
                },
                "title": {
                    "description": "",
                    "type": "sentence"
                },
                "role": {
                    "description": "",
                    "type": "word"
                },
                "notes": {
                    "description": "",
                    "type": "paragraph"
                },
                "users": {
                    "description": "",
                    "type": "array"
                }
            }
        },
        "observation_parse_messages": [
            {"from":"user1", "to":"chat", "message":"some observation"},
            {"from":"assistant", "to":"bot", "message":{"command":"OBSERVE", "data":{ }}},
            {"from":"bot", "to":"assistant", "message":"ok"},
            {"from":"user1", "to":"chat", "message":"some observation"},
            {"from":"assistant", "to":"bot", "message":{"command":"OBSERVE", "data":{ }}},
            {"from":"bot", "to":"assistant", "message":"ok"},
            {"from":"user1", "to":"chat", "message":"some observation"},
            {"from":"assistant", "to":"bot", "message":{"command":"OBSERVE", "data":{ }}},
            {"from":"bot", "to":"assistant", "message":"ok"},
        ],
        "reflect_instructions": "How to reflect as a Chat User",
        "reflect_steps": [
            {
                "step": "deduplicate",
                "prompt": "how to deduplicate as a LLM",
                "instructions": "how to share results and get approval",
                "messages": [
                    {"from":"user1", "to":"chat", "message":"some observation"},
                    {"from":"assistant", "to":"bot", "message":{"command":"OBSERVE", "data":{ }}},
                    {"from":"bot", "to":"assistant", "message":"ok"},
                    {"from":"user1", "to":"chat", "message":"some observation"},
                    {"from":"assistant", "to":"bot", "message":{"command":"OBSERVE", "data":{ }}},
                    {"from":"bot", "to":"assistant", "message":"ok"},
                    {"from":"user1", "to":"chat", "message":"some observation"},
                    {"from":"assistant", "to":"bot", "message":{"command":"OBSERVE", "data":{ }}},
                    {"from":"bot", "to":"assistant", "message":"ok"},
                ]
            },
            {
                "step": "group",
                "prompt": "how to deduplicate as a LLM",
                "instructions": "how to share results and get approval",
                "messages": [
                    {"from":"user1", "to":"chat", "message":"some observation"},
                    {"from":"assistant", "to":"bot", "message":{"command":"OBSERVE", "data":{ }}},
                    {"from":"bot", "to":"assistant", "message":"ok"},
                    {"from":"user1", "to":"chat", "message":"some observation"},
                    {"from":"assistant", "to":"bot", "message":{"command":"OBSERVE", "data":{ }}},
                    {"from":"bot", "to":"assistant", "message":"ok"},
                    {"from":"user1", "to":"chat", "message":"some observation"},
                    {"from":"assistant", "to":"bot", "message":{"command":"OBSERVE", "data":{ }}},
                    {"from":"bot", "to":"assistant", "message":"ok"}
                ]
            },
            {
                "step": "review",
                "prompt": "how to deduplicate as a LLM",
                "instructions": "how to share results and get approval",
                "messages": [
                    {"from":"user1", "to":"chat", "message":"some observation"},
                    {"from":"assistant", "to":"bot", "message":{"command":"OBSERVE", "data":{ }}},
                    {"from":"bot", "to":"assistant", "message":"ok"},
                    {"from":"user1", "to":"chat", "message":"some observation"},
                    {"from":"assistant", "to":"bot", "message":{"command":"OBSERVE", "data":{ }}},
                    {"from":"bot", "to":"assistant", "message":"ok"},
                    {"from":"user1", "to":"chat", "message":"some observation"},
                    {"from":"assistant", "to":"bot", "message":{"command":"OBSERVE", "data":{ }}},
                    {"from":"bot", "to":"assistant", "message":"ok"},
                ]
            }            
        ],
        "reflect_deduplicate_messages": [
        ],
        "reflect_group_messages": [
            {"role":"user", "message":"sample text"},
            {"role":"assistant", "message":"json"},
        ],
        "reflect_prompt": "instructions to guide reflect, one observation at a time",
        "make_instructions": [
            "define scope, then conduct a vote",
            "update workshop document set next exercise name = empathy for {{ .name}}",
            "create new workshops for anyone with a vote, using more_empathy",
        ]
    },
    {},
    {},
    {},
    {}
]