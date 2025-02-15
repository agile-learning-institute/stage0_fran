import logging
import ollama

class Inference:
    
    def __init__(self):
        # Nothing to do here yet
        return
        
    @staticmethod
    def chat(self, model, messages):
        response = ollama.chat(model=model, messages=messages)
        return response
    