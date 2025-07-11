from .base_agent import BaseAgent
from prompts.system_prompts import SystemPrompts

class VPCAgent(BaseAgent):
    def __init__(self):
        super().__init__(SystemPrompts.VPC_PROMPT, "VPC")
