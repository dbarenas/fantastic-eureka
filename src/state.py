from typing import List, Dict, Any

class Turn:
    def __init__(self, role: str, agent_id: str, content: str):
        self.role = role
        self.agent_id = agent_id
        self.content = content

class GraphState:
    def __init__(self, agent_id: str, question: str, messages: List[Turn], context: Dict[str, Any]):
        self.agent_id = agent_id
        self.question = question
        self.messages = messages
        self.context = context
