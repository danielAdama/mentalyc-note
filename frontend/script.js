const outputSection = document.getElementById('output-section');
const sentimentElement = document.getElementById('sentiment');
const gad7AnalysisElement = document.getElementById('gad7-analysis');
const phq9AnalysisElement = document.getElementById('phq9-analysis');
const insightElement = document.getElementById('insight');
const form = document.getElementById('upload-form');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const userId = document.getElementById('user-id').value;
    const files = document.getElementById('session-files').files;

    if (!userId || files.length === 0) {
        alert("Please fill all fields and select files.");
        return;
    }

    const formData = new FormData();
    for (let file of files) {
        formData.append('sessions', file);
    }

    const apiUrl = `http://localhost:8002/v1/therapy/analysis/?user_id=${encodeURIComponent(userId)}`;

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const result = await response.json();
            console.log('API Response:', result);
            displayResults(result.data);
        } else {
            const error = await response.json();
            alert(`Error: ${error.detail || 'Failed to upload files.'}`);
        }
    } catch (err) {
        alert(`Error: ${err.message}`);
    }
});

function displayResults(data) {
    if (!data) {
        alert("No data received from the API.");
        return;
    }

    // Clear previous results
    gad7AnalysisElement.innerHTML = "";
    phq9AnalysisElement.innerHTML = "";

    // Update sentiment
    sentimentElement.textContent = data.sentiment || 'N/A';

    // Update GAD7 analysis
    const gad7Data = data.GAD7_analysis;
    if (gad7Data) {
        gad7AnalysisElement.innerHTML = `<h4>GAD7 Analysis</h4>`; // Add a header for GAD7 analysis
        for (const [session, details] of Object.entries(gad7Data)) {
            const sessionDiv = document.createElement('div');
            sessionDiv.innerHTML = `
                <h5>${session}</h5>
                <p><strong>Total Score:</strong> ${details.total_gad_7_score}</p>
                <p><strong>Severity Classification:</strong> ${details.anxiety_severity_classification}</p>
                <p><strong>Justification:</strong> ${details.justification}</p>
                <p><strong>Scoring Table:</strong></p>
                <ul>
                    ${Object.entries(details.gad_7_scoring_table).map(([key, value]) => `<li>${key}: ${value}</li>`).join('')}
                </ul>
            `;
            gad7AnalysisElement.appendChild(sessionDiv);
        }
    }

    // Update PHQ9 analysis
    const phq9Data = data.PHQ9_analysis;
    if (phq9Data) {
        phq9AnalysisElement.innerHTML = `<h4>PHQ9 Analysis</h4>`; // Add a header for PHQ9 analysis
        for (const [session, details] of Object.entries(phq9Data)) {
            const sessionDiv = document.createElement('div');
            sessionDiv.innerHTML = `
                <h5>${session}</h5>
                <p><strong>Total PHQ-9 Score:</strong> ${details.total_phq_9_score}</p>
                <p><strong>Depression Severity Classification:</strong> ${details.depression_severity_classification}</p>
                <p><strong>Flag for Question 9:</strong> ${details.flag_for_question_9}</p>
                <p><strong>Justification:</strong> ${details.justification}</p>
                <p><strong>PHQ-9 Scoring Table:</strong></p>
                <ul>
                    ${Object.entries(details.phq_9_scoring_table).map(([key, value]) => `<li>${key}: ${value}</li>`).join('')}
                </ul>
            `;
            phq9AnalysisElement.appendChild(sessionDiv);
        }
    }

    // Update insight
    insightElement.textContent = data.insight || 'N/A';
}
