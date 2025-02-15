from flask import request

def create_token():
    """Create a access token from the Discord Environment."""
    return {
        # TODO: Get Values from Discord
        "user_id": "aaaa00000000000000000001",
        "roles": ["Staff"]
    }