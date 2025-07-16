import openai
import ast
from typing import List
from dotenv import load_dotenv
load_dotenv()

AGENT_LIST = [
    {"id": "h3o", "name": "H3O Labs", "description": "Molecule and supplement research expert."},
    {"id": "precision_med", "name": "Precision Medicine", "description": "Human-in-the-loop clinical decision agent."},
    {"id": "mha", "name": "Metabolic Health Advisor", "description": "Nutrition and metabolic disease expert."},
    {"id": "vpc", "name": "Virtual Performance Coach", "description": "Wearable and fitness data specialist."},
    {"id": "dayone", "name": "DayOne Programme", "description": "Longevity intervention specialist."}
]

class MasterRouter:
    def __init__(self):
        self.client = openai.OpenAI()  # Uses OPENAI_API_KEY from environment

    def route_with_llm(self, user_input: str) -> List[str]:
        agent_list_str = "\n".join([f"{a['id']}: {a['name']} - {a['description']}" for a in AGENT_LIST])
        prompt = f"""
You are an intelligent agent router for a medical AI multi-agent system.
User question: "{user_input}"

Agents:
{agent_list_str}

Which agent (use the id) is BEST suited to handle this query?
Return only a valid Python list of agent IDs (e.g., ['h3o', 'precision_med']) as your entire output. Do not include any extra text or explanation.
""".strip()

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            raw_output = response.choices[0].message.content.strip()
            print("LLM raw output:", raw_output)  # Optional: remove in production

            # Only parse if it looks like a Python list
            if raw_output.startswith("[") and raw_output.endswith("]"):
                agent_ids = ast.literal_eval(raw_output)
                if (
                    isinstance(agent_ids, list)
                    and all(a in [x['id'] for x in AGENT_LIST] for a in agent_ids)
                ):
                    return agent_ids

            # Fallback if anything goes wrong
            return ['h3o']
        except Exception as e:
            print("LLM routing failed:", e)
            return ['h3o']

    # Backward compatible methods:
    def classify_input(self, data: str) -> str:
        agents = self.route_with_llm(data)
        return agents[0] if agents else "h3o"

    def get_agents_for_input(self, input_type: str) -> List[str]:
        return self.classify_input(input_type)