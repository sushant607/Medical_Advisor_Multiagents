from .base_agent import BaseAgent
from prompts.system_prompts import SystemPrompts

class PrecisionMedAgent(BaseAgent):
    def __init__(self):
        super().__init__(SystemPrompts.PRECISION_MED_PROMPT, "PrecisionMed")
