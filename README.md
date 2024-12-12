# AI Psychotherapy Progress Notes API

### Description:  
This repository contains a Proof of Concept (POC) for tracking therapy progress using AI-driven assessments. Built for **Mentalyc**, the solution enables psychotherapists to track patient progress by analyzing structured session notes generated from audio recordings. The project utilizes industry-standard psychotherapy tests (e.g., GAD-7, PHQ-9) and multi-agent systems to provide a comprehensive evaluation of symptom progression. 

Key features include:  
- **Structured Assessments**: Leveraging predefined templates to capture and analyze patient data (e.g., SOAP notes).  
- **Symptom Tracking**: AI models detect and compare symptom severity or frequency between sessions to evaluate progress.  
- **Multi-Agent Architecture**: Modular agents tailored for different assessment protocols (GAD-7, PHQ-9, etc.).  
- **Therapist Dashboard**: A simple, FastAPI-powered interface for submitting sessions and visualizing patient progress.  
- **Comprehensive Documentation**: Detailed explanation of the AI approach, design decisions, and instructions for running the solution.

### Approach: Multi-Agent Solution for Therapy Progress Tracking  

This project follows a **Multi-Agent Solution** approach to effectively analyze session data and track therapy progress. Below is a detailed breakdown of the approach:  

#### 1. **Entry Point Node: Sentiment Classification**  
The entry point is a **sentiment classification node** that evaluates the session text templates. This node determines whether the session content reflects signs of:  
   - **Anxiety** (classified as *Anxious*)  
   - **Depression** (classified as *Depressed*)  

The sentiment classification guides subsequent routing based on the predicted emotional state.  

#### 2. **Assessment Router**  
Once the sentiment is classified, the **assessment router** determines the next step:  
   - **If classified as Anxious**: The session data is routed to the **GAD-7 agent**, which specializes in Generalized Anxiety Disorder assessments.  
   - **If classified as Depressed**: The session data is routed to the **PHQ-9 agent**, which specializes in depression assessments.  

#### 3. **GAD-7 and PHQ-9 Agents Nodes**  
These specialized agents assess the client's symptoms based on the industry-standard GAD-7 and PHQ-9 frameworks:  
   - **GAD-7 Agent**: Scores the client’s responses to seven items designed to evaluate the severity of anxiety symptoms.  
   - **PHQ-9 Agent**: Scores the client’s responses to nine items designed to evaluate the severity of depression symptoms.  

Each agent provides:  
   - **Severity Classification**: Determining the level of anxiety or depression.  
   - **Justifications**: Contextual explanations based on the client’s responses.  

#### 4. **Summarizer Node**  
The final step in the pipeline is the **summarizer node**, which performs the following:  
   - **Progress Report Calculation**: Evaluates session-to-session changes to determine if the client’s condition has improved, plateaued, or worsened.  
   - **Summary Generation**: Provides a summary of the session, including actionable insights, therapy progress analysis, and encouragement for the client.  

## Workflow Graph
![agent_graph_workflow](https://github.com/user-attachments/assets/1e85bfa4-b796-48b2-97de-9ba75e76c0d7)

---
### Key Highlights of the Multi-Agent Approach:  
- **Modular Design**: Each node and agent focuses on a specific task, ensuring clarity and flexibility.  
- **Seamless Routing**: Sentiment-based routing ensures that assessments are tailored to the client’s emotional state.  
- **Therapy Progress Insights**: The summarizer node generates actionable insights and a detailed progress analysis for therapists.  

This approach ensures an end-to-end pipeline from sentiment classification to progress reporting, providing psychotherapists with meaningful insights to guide therapy sessions effectively.

---
## Frontend Interface
<img width="1680" alt="mentalyc 4" src="https://github.com/user-attachments/assets/3532d3e6-85e0-409f-a488-aaf4812e2391" />

<img width="1680" alt="mentalyc 5" src="https://github.com/user-attachments/assets/6724dfd9-0e57-4edb-8b3d-1618061139da" />

## Backend Interface

<img width="1680" alt="mentalyc 1" src="https://github.com/user-attachments/assets/4ae64eb7-3f73-42ba-b015-c362b48085f8" />

![mentalyc 3](https://github.com/user-attachments/assets/13bc336d-15a8-43be-ae49-aaec401133e6)

## Project Structure

```
mentalcy-note/
mentalyc_ai
│   ├── __init__.py
│   ├── agents
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── base_agent.py
│   ├── nodes
│   │   ├── __init__.py
│   │   └── node.py
│   ├── prompt
│   │   └── templates
│   │       ├── classifier_system_message.txt
│   │       ├── gad7_system_message.txt
│   │       ├── phq9_system_message.txt
│   │       └── summarizer_system_message.txt
│   ├── routers
│   │   └── router.py
│   ├── schema
│   │   ├── __init__.py
│   │   ├── gad7_schema.py
│   │   ├── phq9_schema.py
│   │   ├── sentiment_schema.py
│   │   ├── state.py
│   │   └── summarize_schema.py
│   └── utils.py
├── frontend/             # Static files for the frontend
│   ├── index.html
│   ├── script.js
│   ├── styles.css
├── prompt/templates/     # System message templates
│   ├── classifier_system_message.txt
│   ├── gad7_system_message.txt
│   ├── phq9_system_message.txt
│   └── summarizer_system_message.txt
├── routers/              # API route definitions
│   ├── __init__.py
│   ├── schema/           # Schema definitions for request/response validation
│   │   └── utils.py
│   └── therapy_service.py
├── src/                  # Source code
│   ├── controllers/      # Controllers for handling requests
│   ├── exceptions/       # Custom exception handlers
│   ├── repositories/     # Database interaction layer
│   ├── schemas/          # Pydantic models for data validation
│   ├── services/         # Core business logic
│   ├── utils/            # Utility functions
│   └── __init__.py
├── app_config.yml        # Configuration file for the application
├── config_helper.py      # Helper functions for configuration
├── logger.py             # Logging configuration
├── main.py               # FastAPI application setup
├── Dockerfile.backend        # Dockerfile for backend
├── Dockerfile.frontend       # Dockerfile for frontend
├── docker-compose.yml        # Docker Compose file
├── Makefile                  # Task management
└── README.md             # Documentation
```
## Explanation of Key Directories and Files

### `mentalyc_ai/`
This is the core application folder containing all backend logic and functionality.

#### `agents/`
- `agent.py`: Contains logic for agent behavior and decision-making.
- `base_agent.py`: Base class for agents with shared functionality.

#### `nodes/`
- `node.py`: Defines nodes used within the application workflow or decision trees.

#### `prompt/templates/`
Contains text-based templates used for various AI model prompts:
- `classifier_system_message.txt`: Template for classifier prompts.
- `gad7_system_message.txt`: Template for GAD-7 prompts.
- `phq9_system_message.txt`: Template for PHQ-9 prompts.
- `summarizer_system_message.txt`: Template for summarization tasks.

#### `routers/`
- `router.py`: Defines API routes for the application.

#### `schema/`
Contains data schemas used for validation and serialization:
- `gad7_schema.py`: Schema for GAD-7-related data.
- `phq9_schema.py`: Schema for PHQ-9-related data.
- `sentiment_schema.py`: Schema for sentiment-related data.
- `state.py`: Defines state management logic.
- `summarize_schema.py`: Schema for summarization tasks.

### Frontend
A simple static frontend for user interaction.
- `index.html`: HTML structure of the application.
- `script.js`: JavaScript logic for the frontend.
- `styles.css`: Styling for the frontend.

### Entry Points
- `mentalyc_ai.py`: Main script to launch the Mentalyc AI functionality.
- `main.py`: Entry point to start the FastAPI application.

---

## How to Use
---

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.10+
- pip (Python package installer)
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**:

```bash
git clone https://github.com/danielAdama/mentalcy-note.git
cd mentalcy-note
```

2. **Install dependencies**:

```bash
poetry install
```

3. **Configure the application**:

Edit `app_config.yml` to set up any required configurations.

4. **Verify**  
   - The backend API should be running at `http://localhost:8002/docs`.
   - The frontend should be accessible at `http://localhost:8081`.

### Running the Application

#### Locally

Run the FastAPI application using:

```bash
make start_dev
```

The API will be available at [http://localhost:8002](http://localhost:8002).

#### Docker

1. Build the Docker image:

```bash
make compose_up
```

2. Run the container:

```bash
make compose_up
```

---

## API Endpoints

### Root Endpoint

- **GET** `/`
  - **Description**: Check the status of the API.
  - **Response**:
    ```json
    {
      "message": "Mentalyc Service API is RUNNING!"
    }
    ```

### Therapy Service

- **POST** `http://localhost:8002/v1/therapy/analysis/?user_id=<user_id>`
  - **Description**: Handles therapeutic-related routes and services.
  - **Response**:
    ```json
    {
    "code": 200,
    "message": "Progress tracked successfully",
    "data": {
        "sentiment": "anxious",
        "GAD7_analysis": {
            "session1": {
                "gad_7_scoring_table": {
                    "Feeling nervous, anxious, or on edge": 2,
                    "Not being able to stop or control worrying": 2,
                    "Worrying too much about different things": 2,
                    "Trouble relaxing": 1,
                    "Being so restless that it's hard to sit still": 1,
                    "Becoming easily annoyed or irritable": 1,
                    "Feeling afraid as if something awful might happen": 1
                },
                "total_gad_7_score": 10,
                "anxiety_severity_classification": "Moderate anxiety",
                "justification": "The client reported experiencing symptoms of anxiety, including feeling nervous and anxious, worrying too much, and having trouble relaxing, over the past six weeks. These align with moderate anxiety severity based on the GAD-7 scoring criteria."
            },
            "session2": {
                "gad_7_scoring_table": {
                    "Feeling nervous, anxious, or on edge": 1,
                    "Not being able to stop or control worrying": 1,
                    "Worrying too much about different things": 1,
                    "Trouble relaxing": 1,
                    "Being so restless that it's hard to sit still": 0,
                    "Becoming easily annoyed or irritable": 0,
                    "Feeling afraid as if something awful might happen": 0
                },
                "total_gad_7_score": 4,
                "anxiety_severity_classification": "Mild anxiety",
                "justification": "The client reported a significant reduction in anxiety and stress, with improved task management and boundary-setting. His symptoms have decreased following the application of therapy strategies, indicating mild anxiety severity based on the GAD-7 scoring criteria."
            }
        },
        "insight": "### Assessment Summary\nThe client underwent a GAD-7 assessment, which measures the severity of generalized anxiety disorder symptoms. Between Session 1 and Session 2, the client's severity classification improved from \"Moderate anxiety\" to \"Mild anxiety.\" Initially, the client reported experiencing several symptoms of anxiety, including feeling nervous, worrying too much, and having trouble relaxing, which aligned with moderate anxiety severity. However, by Session 2, the client showed a significant reduction in anxiety and stress levels, attributed to improved task management, boundary-setting, and the application of therapy strategies. This progress led to a reclassification to mild anxiety severity.\n\n### Progress Analysis\nThe progress report across sessions indicates the following changes in symptoms:\n- **Feeling nervous, anxious, or on edge:** Improvement\n- **Not being able to stop or control worrying:** Improvement\n- **Worrying too much about different things:** Improvement\n- **Trouble relaxing:** Plateau\n- **Being so restless that it's hard to sit still:** Improvement\n- **Becoming easily annoyed or irritable:** Improvement\n- **Feeling afraid as if something awful might happen:** Improvement\n- **Total score:** Improvement\n\nOverall, the client has shown significant improvement in most anxiety symptoms, with the total score reflecting this positive trend. However, the symptom of \"trouble relaxing\" has plateaued, indicating a need for targeted strategies to address this specific issue.\n\n### Actionable Insights\nTo sustain the improvements and address the plateau:\n- For symptoms showing improvement, continue and possibly intensify the current therapy strategies and stress management techniques, as they seem to be effective.\n- For \"trouble relaxing,\" which has plateaued, consider introducing or enhancing relaxation techniques such as deep breathing exercises, progressive muscle relaxation, or mindfulness meditation. Regular practice of these techniques could help improve the client's ability to relax.\n- It might also be beneficial to explore the underlying reasons for the difficulty in relaxing, which could be related to unresolved issues, unmanaged stress, or physical discomfort. Addressing these underlying factors could be crucial anxiety.\n\n### Encouragement\nIt's truly commendable to see the significant progress made between sessions, reflecting the client's hard work and dedication to their mental health. The improvement in anxiety symptoms is a testament to the effectiveness of the applied strategies and the client's resilience. Continuing on this path, with a focus on overcoming the remaining challenges, such as trouble relaxing, will be key to further progress. Remember, mental health is a journey, and it's okay to take it one step at a time. Keep moving forward, and don't hesitate to seek support when needed."
    }
    ```

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazingfeat`)
3. Commit your changes (`git commit -m 'add: some amazingfeat'`)
4. Push to the branch (`git push origin feature/amazingfeat`)
5. Open a pull request

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact

For inquiries, please contact Daniel Enemona Adama at [adamadaniel321@gmail.com](mailto:adamadaniel321@gmail.com).
