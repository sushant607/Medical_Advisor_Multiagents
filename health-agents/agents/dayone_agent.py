from .base_agent import BaseAgent
from prompts.system_prompts import SystemPrompts

class DayOneAgent(BaseAgent):
    def __init__(self):
        super().__init__(SystemPrompts.DAYONE_PROMPT, "DayOne")
