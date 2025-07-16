from .base_agent import BaseAgent
from prompts.system_prompts import SystemPrompts
import json
import logging
from typing import Dict, Any, List, Optional

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(SystemPrompts.ORCHESTRATOR_PROMPT, "Orchestrator")
        self.logger = logging.getLogger(__name__)
        
        # Agent routing configuration
        self.agent_domains = {
            "h3o": ["metabolic_analysis", "supplement_recommendations", "biomarker_interpretation"],
            "psychology": ["behavioral_patterns", "motivation", "stress_management", "adherence_support"],
            "mha": ["habit_tracking", "real_time_coaching", "lifestyle_optimization"],
            "vpc": ["exercise_programming", "recovery_optimization", "performance_tracking"],
            "precision_med": ["clinical_oversight", "safety_validation", "medical_guidelines"],
            "dayone": ["program_coordination", "phase_management", "weekly_planning"]
        }
        
        # Phase-specific agent priorities
        self.phase_priorities = {
            "Observation": ["h3o", "psychology", "mha"],
            "Experimentation": ["psychology", "precision_med", "h3o"],
            "Metabolic Acceleration": ["h3o", "vpc", "mha"],
            "Metabolic Accountability and Plateau Defense": ["psychology", "vpc", "mha"],
            "Metabolic Review": ["psychology", "h3o", "dayone"]
        }

    def _format_input(self, data: str, context: Dict[str, Any] = None) -> str:
        """Enhanced input formatting for orchestration analysis"""
        formatted = f"User Query: {data}\n\n"
        
        if context:
            current_phase = context.get("current_phase", "Unknown")
            user_data = context.get("user_data", {})
            available_agents = context.get("available_agents", [])
            
            formatted += f"**Orchestration Context:**\n"
            formatted += f"Current Phase: {current_phase}\n"
            formatted += f"Available Agents: {', '.join(available_agents)}\n"
            
            if user_data:
                formatted += f"User Data: {json.dumps(user_data, indent=2)}\n"
            
            formatted += "\n"
        
        formatted += "**Required Output:** Provide structured JSON response with agent coordination plan, task distribution, and synthesis strategy.\n"
        
        return formatted

    def analyze_and_route(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze input and determine optimal agent routing"""
        try:
            response = self.process(user_input, context)
            
            # Attempt to parse JSON response
            try:
                parsed_response = json.loads(response)
                
                # Validate required fields
                required_fields = ["phase", "recommendation", "agents_involved"]
                if all(field in parsed_response for field in required_fields):
                    return parsed_response
                else:
                    return self._create_fallback_routing(context, user_input)
                    
            except json.JSONDecodeError:
                # Create routing based on keyword analysis
                return self._analyze_routing_keywords(user_input, context)
                
        except Exception as e:
            self.logger.error(f"Error in orchestration analysis: {str(e)}")
            return self._create_error_routing(context, str(e))

    def _analyze_routing_keywords(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze keywords to determine agent routing"""
        current_phase = context.get("current_phase", "Unknown") if context else "Unknown"
        user_input_lower = user_input.lower()
        
        # Determine relevant agents based on keywords
        relevant_agents = []
        
        # Psychology keywords
        if any(keyword in user_input_lower for keyword in ["stress", "motivation", "anxiety", "mood", "behavior", "habit"]):
            relevant_agents.append("psychology")
        
        # Medical/supplement keywords
        if any(keyword in user_input_lower for keyword in ["supplement", "dose", "side effect", "glp-1", "medication"]):
            relevant_agents.extend(["h3o", "precision_med"])
        
        # Exercise keywords
        if any(keyword in user_input_lower for keyword in ["exercise", "workout", "training", "recovery", "muscle"]):
            relevant_agents.append("vpc")
        
        # Habit/lifestyle keywords
        if any(keyword in user_input_lower for keyword in ["habit", "routine", "tracking", "daily", "lifestyle"]):
            relevant_agents.append("mha")
        
        # Default to phase-specific agents if no specific keywords found
        if not relevant_agents:
            relevant_agents = self.phase_priorities.get(current_phase, ["h3o", "psychology"])
        
        return {
            "phase": current_phase,
            "recommendation": f"Route to {', '.join(relevant_agents)} for comprehensive analysis",
            "agents_involved": relevant_agents,
            "vote_summary": {
                "agent_scores": {agent: 8 for agent in relevant_agents},
                "consensus_level": "85%",
                "final_decision": "Keyword-based routing with phase consideration"
            },
            "escalation_triggers": "none",
            "confidence_score": 7
        }

    def _create_fallback_routing(self, context: Dict[str, Any] = None, user_input: str = "") -> Dict[str, Any]:
        """Create fallback routing when parsing fails"""
        current_phase = context.get("current_phase", "Unknown") if context else "Unknown"
        default_agents = self.phase_priorities.get(current_phase, ["h3o", "psychology"])
        
        return {
            "phase": current_phase,
            "recommendation": "Standard multi-agent consultation with phase-appropriate specialists",
            "agents_involved": default_agents,
            "vote_summary": {
                "agent_scores": {agent: 6 for agent in default_agents},
                "consensus_level": "70%",
                "final_decision": "Fallback to phase-specific agent routing"
            },
            "escalation_triggers": "parsing_issue",
            "confidence_score": 5
        }

    def _create_error_routing(self, context: Dict[str, Any] = None, error_msg: str = "Unknown error") -> Dict[str, Any]:
        """Create error routing response"""
        return {
            "phase": "Error",
            "recommendation": "System error - escalate to human concierge immediately",
            "agents_involved": ["precision_med"],
            "vote_summary": {
                "agent_scores": {"precision_med": 10},
                "consensus_level": "100%",
                "final_decision": "Emergency escalation due to system error"
            },
            "escalation_triggers": "system_error_immediate",
            "confidence_score": 10
        }

    def synthesize_agent_responses(self, agent_responses: Dict[str, Any], user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Synthesize multiple agent responses into unified recommendation"""
        try:
            # Calculate consensus and scores
            total_score = 0
            agent_count = 0
            consensus_items = []
            
            for agent_name, response in agent_responses.items():
                if isinstance(response, dict) and "relevance_score" in response:
                    total_score += response["relevance_score"]
                    agent_count += 1
                    
                    # Extract key recommendations
                    if "motivational_strategy" in response:
                        consensus_items.append(response["motivational_strategy"])
                    elif "recommendation" in response:
                        consensus_items.append(response["recommendation"])
            
            average_score = total_score / agent_count if agent_count > 0 else 5
            consensus_level = f"{min(average_score * 10, 100):.0f}%"
            
            # Create synthesized recommendation
            synthesized_recommendation = self._create_synthesized_plan(consensus_items, user_context)
            
            return {
                "phase": user_context.get("current_phase", "Unknown") if user_context else "Unknown",
                "recommendation": synthesized_recommendation,
                "agents_involved": list(agent_responses.keys()),
                "vote_summary": {
                    "agent_scores": {name: resp.get("relevance_score", 5) for name, resp in agent_responses.items()},
                    "consensus_level": consensus_level,
                    "final_decision": "Multi-agent synthesis with weighted scoring"
                },
                "escalation_triggers": self._check_escalation_needs(agent_responses),
                "confidence_score": min(int(average_score), 10)
            }
            
        except Exception as e:
            self.logger.error(f"Error in response synthesis: {str(e)}")
            return self._create_error_routing(user_context, str(e))

    def _create_synthesized_plan(self, consensus_items: List[str], user_context: Dict[str, Any] = None) -> str:
        """Create a synthesized action plan from multiple agent inputs"""
        if not consensus_items:
            return "Comprehensive assessment recommended with multi-agent consultation"
        
        # Prioritize based on current phase
        current_phase = user_context.get("current_phase", "Unknown") if user_context else "Unknown"
        
        phase_focus = {
            "Observation": "Focus on baseline establishment and habit formation",
            "Experimentation": "Prioritize tolerance building and side effect management",
            "Metabolic Acceleration": "Emphasize momentum maintenance and progress optimization",
            "Metabolic Accountability and Plateau Defense": "Concentrate on resilience building and plateau navigation",
            "Metabolic Review": "Focus on sustainability planning and maintenance strategies"
        }
        
        base_plan = phase_focus.get(current_phase, "Implement comprehensive metabolic health approach")
        
        # Combine top recommendations
        top_recommendations = consensus_items[:3]  # Limit to top 3 to avoid overwhelm
        combined_plan = f"{base_plan}. Key actions: {'; '.join(top_recommendations)}"
        
        return combined_plan

    def _check_escalation_needs(self, agent_responses: Dict[str, Any]) -> str:
        """Check if any agent responses indicate need for escalation"""
        escalation_triggers = []
        
        for agent_name, response in agent_responses.items():
            if isinstance(response, dict):
                # Check for emergency indicators
                if response.get("relevance_score", 0) >= 9:
                    escalation_triggers.append(f"high_priority_{agent_name}")
                
                # Check for specific escalation flags
                if "escalation" in str(response).lower():
                    escalation_triggers.append(f"agent_escalation_{agent_name}")
                
                # Check for error conditions
                if "error" in str(response).lower():
                    escalation_triggers.append(f"error_condition_{agent_name}")
        
        return ", ".join(escalation_triggers) if escalation_triggers else "none"

    def coordinate_agent_debate(self, topic: str, participating_agents: List[str], user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Coordinate multi-agent debate on specific topics"""
        debate_prompt = f"""
        **Multi-Agent Debate Topic:** {topic}
        
        **Participating Agents:** {', '.join(participating_agents)}
        
        **User Context:** {json.dumps(user_context, indent=2) if user_context else 'Not provided'}
        
        **Instructions:** Facilitate a structured debate where each agent provides their perspective on the topic, considering the user's specific context and program phase. Score each perspective for relevance and evidence quality.
        """
        
        try:
            response = self.process(debate_prompt, user_context)
            
            return {
                "debate_topic": topic,
                "participating_agents": participating_agents,
                "debate_summary": response,
                "consensus_reached": "partial",  # Would need more sophisticated analysis
                "next_steps": "Implement highest-scoring recommendations with monitoring"
            }
            
        except Exception as e:
            self.logger.error(f"Error in agent debate coordination: {str(e)}")
            return {
                "debate_topic": topic,
                "participating_agents": participating_agents,
                "debate_summary": f"Debate coordination failed: {str(e)}",
                "consensus_reached": "failed",
                "next_steps": "Escalate to human concierge for manual coordination"
            }
