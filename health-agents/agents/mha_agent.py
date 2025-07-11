from .base_agent import BaseAgent
from prompts.system_prompts import SystemPrompts

class MHAAgent(BaseAgent):
    def __init__(self):
        super().__init__(SystemPrompts.MHA_PROMPT, "MHA")
