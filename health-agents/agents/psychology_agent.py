from .base_agent import BaseAgent
from prompts.system_prompts import SystemPrompts
import json
import logging
from typing import Dict, Any, Optional

class PsychologyAgent(BaseAgent):
    def __init__(self):
        super().__init__(SystemPrompts.PSYCHOLOGY_PROMPT, "Psychology")
        self.logger = logging.getLogger(__name__)
        
        