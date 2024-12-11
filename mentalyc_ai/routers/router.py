def assessment_router(state):
    classification = state["messages"][-1].content
    if "anxious" in classification:
        return "gad7_agent"
    elif "depressed" in classification:
        return "phq9_agent"
    else:
        return None