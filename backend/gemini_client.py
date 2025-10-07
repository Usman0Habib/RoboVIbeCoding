import google.generativeai as genai
import os
import json

class GeminiClient:
    def __init__(self):
        self.api_key = None
        self.model = None
        self.configured = False
        
        settings_path = 'config/settings.json'
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                settings = json.load(f)
                if 'gemini_api_key' in settings:
                    self.set_api_key(settings['gemini_api_key'])
    
    def set_api_key(self, api_key):
        self.api_key = api_key
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.configured = True
        except Exception as e:
            self.configured = False
            raise Exception(f"Failed to configure Gemini: {str(e)}")
    
    def generate_response(self, prompt, context=None):
        if not self.configured:
            return "⚠️ Gemini API not configured. Please add your API key in settings."
        
        try:
            full_prompt = prompt
            if context:
                full_prompt = f"{context}\n\n{prompt}"
            
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def generate_response_stream(self, prompt, context=None):
        if not self.configured:
            yield "⚠️ Gemini API not configured. Please add your API key in settings."
            return
        
        try:
            full_prompt = prompt
            if context:
                full_prompt = f"{context}\n\n{prompt}"
            
            response = self.model.generate_content(full_prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"Error generating response: {str(e)}"
