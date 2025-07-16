import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class BaseAgent:
    def __init__(self, system_prompt: str, agent_name: str):
        self.api_key = os.getenv('XAI_GROK_API_KEY')
        self.api_url = 'https://api.x.ai/v1/chat/completions'
        self.system_prompt = system_prompt
        self.agent_name = agent_name

    def process(self, user_data: str, context: Dict[str, Any] = None) -> str:
        """Process user input through the agent using xAI Grok-4."""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self._format_input(user_data, context)}
        ]
        data = {
            "model": "grok-4-0709",
            "messages": messages,
            "temperature": 0.7,
        }
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error: {response.status_code}, {response.text}"
        except Exception as e:
            return f"Error processing with {self.agent_name}: {str(e)}"

    def _format_input(self, data: str, context: Dict[str, Any]) -> str:
        formatted = f"User Input: {data}\n\n"
        if context:
            formatted += f"Context: {context}\n\n"
        return formatted
