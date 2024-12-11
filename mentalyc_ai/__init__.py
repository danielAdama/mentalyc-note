from src.utils.app_utils import AppUtil
from .nodes.node import Node
from .agents.agent import Agent
from .schema import gad7_schema, phq9_schema, sentiment_schema, state
from pathlib import Path
from .routers.router import assessment_router
from langgraph.graph import END, StateGraph

class MentalycNoteAgent:
    """
    MentalycNoteAgent is a class that manages the workflow of various agents for mental health analysis.
    It initializes agents, sets up system messages, and defines the workflow graph for processing sessions.

    Attributes:
        BASE_DIR (Path): The base directory of the project.
        PROMPT_DIR (Path): The directory containing prompt templates.
    """
    
    BASE_DIR = Path('__file__').absolute().parent
    PROMPT_DIR = BASE_DIR / "mentalyc_ai" / "prompt" / "templates"

    def __init__(self, user_id):
        """
        Initializes the MentalycNoteAgent with the given user ID.

        Args:
            user_id (str): The unique identifier for the user.
        """
        self.user_id = user_id
        self.initialize_system_messages()
        self.initialize_agents()
        self.nodes = Node(
            self.sentiment_classifier_instance,
            self.summarizer_instance,
            self.gad7_instance,
            self.phq9_instance
        )
        self.flow = self.initialize_graph()

    def initialize_agents(self):
        """
        Initializes the various agents required for the workflow.
        """
        self.sentiment_classifier_agent = self.create_agent(
            Agent, "ClassifierAgent", self.classifier_system_message, sentiment_schema.SentimentClassificationOutput
        )
        self.gad7_agent = self.create_agent(
            Agent, "GAD7Agent", self.gad7_system_message, gad7_schema.GAD7Output
        )
        self.phq9_agent = self.create_agent(
            Agent, "PHQ9Agent", self.phq9_system_message, phq9_schema.PHQ9Output
        )
        self.summarizer_agent = self.create_agent(
            Agent, "SummarizerAgent", self.summarizer_system_message, None
        )

        self.sentiment_classifier_instance = self.sentiment_classifier_agent.get_agent()
        self.summarizer_instance = self.summarizer_agent.get_agent()
        self.gad7_instance = self.gad7_agent.get_agent()
        self.phq9_instance = self.phq9_agent.get_agent()

    def initialize_system_messages(self):
        """
        Loads system messages for the agents from the prompt templates directory.
        """
        self.classifier_system_message = AppUtil.load_file(self.PROMPT_DIR / 'classifier_system_message.txt')
        self.gad7_system_message = AppUtil.load_file(self.PROMPT_DIR / 'gad7_system_message.txt')
        self.phq9_system_message = AppUtil.load_file(self.PROMPT_DIR / 'phq9_system_message.txt')
        self.summarizer_system_message = AppUtil.load_file(self.PROMPT_DIR / 'summarizer_system_message.txt')

    def create_agent(self, agent_class, name, system_message, schema=None, **kwargs):
        """
        Creates an agent instance with the given parameters.

        Args:
            agent_class (class): The class of the agent to be created.
            name (str): The name of the agent.
            system_message (str): The system message for the agent.
            schema (Optional[Type]): The schema for the agent's output.
            **kwargs: Additional keyword arguments for the agent.

        Returns:
            Agent: The created agent instance.
        """
        return agent_class(
            name=name,
            schema=schema,
            system_message=system_message,
            **kwargs
        )

    def initialize_graph(self):
        """
        Initializes the workflow graph for the agents.

        Returns:
            CompiledStateGraph: The compiled workflow graph.
        """
        workflow = StateGraph(state.AgentState)

        workflow.add_node("sentiment_classifier_agent", self.nodes.sentiment_classifier_node)
        workflow.add_node("gad7_agent", self.nodes.gad7_node)
        workflow.add_node("phq9_agent", self.nodes.phq9_node)
        workflow.add_node("summarizer", self.nodes.summarizer_node)
        workflow.add_conditional_edges(
            source="sentiment_classifier_agent",
            path=assessment_router,
            path_map={"gad7_agent": "gad7_agent", "phq9_agent": "phq9_agent"}#, "__end__": "__end__"}
        )

        workflow.add_edge("gad7_agent", "summarizer")
        workflow.add_edge("phq9_agent", "summarizer")
        workflow.add_edge("summarizer", END)

        workflow.set_entry_point("sentiment_classifier_agent")
        return workflow.compile()
    
    def __call__(self, sessions):
        """
        Invokes the workflow with the given sessions and returns the summarized output.

        Args:
            sessions (List[Dict[str, Any]]): The sessions to be processed.

        Returns:
            str: The summarized output from the SummarizerAgent.
        """
        print(sessions)
        output=self.flow.invoke({"sessions": sessions, "user": self.user_id})
        message = output["messages"][0]
        if message.name == "SummarizerAgent":
            return message.content