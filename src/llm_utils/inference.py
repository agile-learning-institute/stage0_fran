import logging
import ollama

class Inference:
    model = ""
    
    def __init__(self, modelfile):
        # load model from ?
        self.model = 'llama3.2:latest'
        return
        
    @staticmethod
    def chat(self, messages):
        response = ollama.chat(model=self.model, messages=messages)
        return response
    
    