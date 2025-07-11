from .base_agent import BaseAgent
from prompts.system_prompts import SystemPrompts

class H3OAgent(BaseAgent):
    def __init__(self):
        super().__init__(SystemPrompts.H3O_PROMPT, "H3O")

    def synthesize_recommendations(self, agent_responses):
        # Example: simple aggregation
        return "\n\n".join(agent_responses)
