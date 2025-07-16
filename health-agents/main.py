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

    def process_user_input(self, user_data: str, *args, **kwargs) -> str:
        print("***** PATCHED: process_user_input is running *****")
        print("ARGS:", args, "KWARGS:", kwargs)
        agent_name = self.router.classify_input(user_data)
        if agent_name not in self.agents:
            return f"No suitable agent found for input: {agent_name}"
        result = self.agents[agent_name].process(user_data)
        return result

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
