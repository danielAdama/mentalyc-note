const apiUrl = "http://localhost:8001/v1/image/classify/";

document.getElementById('uploadForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const response = await fetch(apiUrl, {
        method: 'POST',
        body: formData
    });

    const result = await response.json();

    document.getElementById('prediction').textContent = result.data.prediction;
    document.getElementById('probability').textContent = result.data.probability.toFixed(2);
    document.getElementById('label').textContent = result.data.label;
    document.getElementById('latency').textContent = result.data.latency.toFixed(4);
    document.getElementById('throughput').textContent = result.data.throughput.toFixed(4);

    // Display the uploaded image
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById('uploadedImage').src = e.target.result;
    };
    reader.readAsDataURL(file);
});
