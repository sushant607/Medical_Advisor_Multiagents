from agents.h3o_agent import H3OAgent
from agents.dayone_agent import DayOneAgent
from agents.mha_agent import MHAAgent
from agents.vpc_agent import VPCAgent
from agents.precision_med_agent import PrecisionMedAgent
from router.master_router import MasterRouter

class HealthAgentNetwork:
    def __init__(self):
        self.agents = {
            'h3o': H3OAgent(),
            'dayone': DayOneAgent(),
            'mha': MHAAgent(),
            'vpc': VPCAgent(),
            'precision_med': PrecisionMedAgent()
        }
        self.router = MasterRouter()

    def process_user_input(self, user_data: str, data_type: str = None) -> str:
        if not data_type:
            data_type = self.router.classify_input(user_data)
        agent_names = self.router.get_agents_for_input(data_type)
        agent_results = []
        for agent_name in agent_names:
            if agent_name in self.agents:
                result = self.agents[agent_name].process(user_data)
                agent_results.append({
                    'agent': agent_name,
                    'response': result
                })
        if len(agent_results) > 1:
            synthesis_data = [f"**{r['agent'].upper()}**: {r['response']}" for r in agent_results]
            final_response = self.agents['h3o'].synthesize_recommendations(synthesis_data)
            return final_response
        return agent_results[0]['response'] if agent_results else "No agents available to process this request."

if __name__ == "__main__":
    network = HealthAgentNetwork()
    print("🏥 Health Agent Network Ready!")
    print("Enter your health data, questions, or type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = network.process_user_input(user_input)
        print(f"\n🤖 AI Response:\n{response}\n")
        print("-" * 50)
