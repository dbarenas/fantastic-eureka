import sys
from .state import GraphState
from .agents import researcher

def main():
    if len(sys.argv) > 1:
        question = sys.argv[1]
        initial_state = GraphState(agent_id="test-agent", question=question, messages=[], context={})
        final_state = researcher(initial_state)
        print(final_state.messages[-1].content)

if __name__ == "__main__":
    main()
