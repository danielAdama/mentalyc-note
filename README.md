# mentalyc-note
# Mentalyc Service API

Mentalyc Service API is a FastAPI-based backend service designed to support therapeutic and mental health assessment solutions. The application incorporates multi-agent architecture and facilitates functionalities such as text summarization, classification, and session tracking.

---

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
└── README.md             # Documentation
```

---

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.9+
- pip (Python package installer)
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/mentalcy-note.git
cd mentalcy-note
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the application:

Edit `app_config.yml` to set up any required configurations.

### Running the Application

#### Locally

Run the FastAPI application using:

```bash
uvicorn main:app --reload
```

The API will be available at [http://localhost:8002](http://localhost:8002).

#### Docker

1. Build the Docker image:

```bash
docker build -t mentalcy-service .
```

2. Run the container:

```bash
docker run -p 8000:8000 mentalcy-service
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
3. Commit your changes (`git commit -m 'Add some amazingfeat'`)
4. Push to the branch (`git push origin feature/amazingfeat`)
5. Open a pull request

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact

For inquiries, please contact Daniel Enemona Adama at [adamadaniel321@gmail.com](mailto:adamadaniel321@gmail.com).
