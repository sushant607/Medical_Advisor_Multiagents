import anthropic
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class BaseAgent:
    def __init__(self, system_prompt: str, agent_name: str):
        self.client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
        self.system_prompt = system_prompt
        self.agent_name = agent_name

    def process(self, user_data: str, context: Dict[str, Any] = None) -> str:
        """Process user input through the agent"""
        try:
            formatted_input = self._format_input(user_data, context)
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                system=self.system_prompt,
                messages=[{
                    "role": "user",
                    "content": formatted_input
                }]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error processing with {self.agent_name}: {str(e)}"

    def _format_input(self, data: str, context: Dict[str, Any]) -> str:
        formatted = f"User Input: {data}\n\n"
        if context:
            formatted += f"Context: {context}\n\n"
        return formatted
