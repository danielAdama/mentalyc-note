from langchain_core.messages import (
    AIMessage,
    HumanMessage
)
import functools
import json

class Node:
    """
    Node class manages the workflow nodes for various agents in the mental health analysis system.
    It handles the invocation of agents and the processing of session data.

    Attributes:
        sentiment_classifier_instance (Agent): Instance of the sentiment classifier agent.
        summarizer_instance (Agent): Instance of the summarizer agent.
        gad7_instance (Agent): Instance of the GAD-7 agent.
        phq9_instance (Agent): Instance of the PHQ-9 agent.
    """
    def __init__(self, sentiment_classifier_instance, summarizer_instance, gad7_instance, phq9_instance):
        """
        Initializes the Node with the given agent instances.

        Args:
            sentiment_classifier_instance (Agent): Instance of the sentiment classifier agent.
            summarizer_instance (Agent): Instance of the summarizer agent.
            gad7_instance (Agent): Instance of the GAD-7 agent.
            phq9_instance (Agent): Instance of the PHQ-9 agent.
        """
        self.sentiment_classifier_instance = sentiment_classifier_instance
        self.summarizer_instance = summarizer_instance
        self.gad7_node = functools.partial(
            self.agent_node, instance=gad7_instance, agent_name="GAD7Agent", completion_message="GAD-7 analysis complete"
        )
        self.phq9_node = functools.partial(
            self.agent_node, instance=phq9_instance, agent_name="PHQ9Agent", completion_message="PHQ-9 analysis complete"
        )

    def sentiment_classifier_node(self, state):
        """
        Processes the sentiment classification node.

        Args:
            state (dict): The current state of the workflow.

        Returns:
            dict: The updated state after processing the sentiment classification.
        """
        name = "ClassifierAgent"
        session = state.get("sessions", {}).get('session1')
        user = state.get('user')

        if not session:
            raise ValueError("Session data not found")

        output = self.invoke_instance(self.sentiment_classifier_instance, session)
        result = AIMessage(content=json.loads(output.model_dump_json())['classification'], name=name)
        return {
            "messages": [result],
            "user": user,
            "session_results": {},
            "stage": name
        }
    
    def summarizer_node(self, state):
        """
        Processes the summarizer node.

        Args:
            state (dict): The current state of the workflow.

        Returns:
            dict: The updated state after processing the summarizer.
        """
        name = "SummarizerAgent"
        user = state.get("user")
        session_results = state.get("session_results", {})

        progress_report = self.analyze_report(session_results)
        output = self.invoke_instance(self.summarizer_instance, progress_report)

        return {
            "messages": [AIMessage(content=output.content, name=name)],
            "user": user,
            "stage": name,
            "session_results": session_results
        }

    def agent_node(self, state, instance, agent_name, completion_message):
        """
        Processes a generic agent node.

        Args:
            state (dict): The current state of the workflow.
            instance (Agent): The agent instance to be invoked.
            agent_name (str): The name of the agent.
            completion_message (str): The completion message for the agent.

        Returns:
            dict: The updated state after processing the agent node.
        """
        sessions = state.get("sessions", {})
        user = state.get("user")
        session_results = state.get("session_results", {})

        for session_id, session_data in sessions.items():
            output = self.invoke_instance(instance, session_data)
            session_results[session_id] = json.loads(output.model_dump_json())

        return {
            "messages": [AIMessage(content=completion_message, name=agent_name)],
            "user": user,
            "stage": agent_name,
            "session_results": session_results
        }

    def invoke_instance(self, instance, session_data):
        """
        Invokes the given agent instance with the session data.

        Args:
            instance (Agent): The agent instance to be invoked.
            session_data (dict): The session data to be processed.

        Returns:
            AIMessage: The output message from the agent.
        """
        output = instance.invoke(
            {
                "messages": [HumanMessage(content=json.dumps(session_data))]
            }
        )
        return output

    def analyze_report(self, sessions):
        """
        Analyzes the progress report across sessions.

        Args:
            sessions (dict): The sessions to be analyzed.

        Returns:
            list: The list of progress reports.
        """
        progress_reports = []
        session_keys = sorted(sessions.keys())

        for i in range(1, len(session_keys)):
            session1 = sessions[session_keys[i-1]]
            session2 = sessions[session_keys[i]]
            progress = {}

            # Determine the type of scoring table and total score key
            if 'gad_7_scoring_table' in session1:
                scoring_table_key = 'gad_7_scoring_table'
                total_score_key = 'total_gad_7_score'
                severity_classification_key = 'anxiety_severity_classification'
                assessment_type = 'GAD-7'
            elif 'phq_9_scoring_table' in session1:
                scoring_table_key = 'phq_9_scoring_table'
                total_score_key = 'total_phq_9_score'
                severity_classification_key = 'depression_severity_classification'
                assessment_type = 'PHQ-9'
            else:
                raise ValueError("Unsupported session data format")

            # Compare scores for each symptom
            for symptom, score1 in session1[scoring_table_key].items():
                score2 = session2[scoring_table_key][symptom]
                if score2 < score1:
                    progress[symptom] = "Improvement"
                elif score2 > score1:
                    progress[symptom] = "Deterioration"
                else:
                    progress[symptom] = "Plateau"

            # Analyze total score
            total_score_diff = session2[total_score_key] - session1[total_score_key]
            if total_score_diff < 0:
                progress["total_score"] = "Improvement"
            elif total_score_diff > 0:
                progress["total_score"] = "Deterioration"
            else:
                progress["total_score"] = "Plateau"

            # Create the session details report
            session_details = {
                session_keys[i-1]: {
                    "severity_classification": session1[severity_classification_key],
                    "justification": session1.get("justification", "No justification provided")
                },
                session_keys[i]: {
                    "severity_classification": session2[severity_classification_key],
                    "justification": session2.get("justification", "No justification provided")
                },
                'progress_report_across_sessions': progress
            }

            progress_reports.append({
                "assessment_type": assessment_type,
                "session_details": session_details
            })

        return progress_reports