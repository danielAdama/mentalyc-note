from typing import Annotated, List, Dict, Any, TypedDict
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    stage: str #"The current stage or state of the agent"]
    user: str #"Unique identifier for the user"]
    sessions: Dict[str, Any] #"Store multiple sessions with keys like 'session_1' and 'session_2'"]
    messages: List[BaseMessage] #"List of messages related to the agent's interactions"]
    session_results: Dict[str, Any] #"Store the analyzed results for sessions"]