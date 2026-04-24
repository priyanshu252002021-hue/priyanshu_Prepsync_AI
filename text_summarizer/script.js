const API_URL = "http://127.0.0.1:8000";

let extractedText = "";

// Upload PDF → send to backend
async function uploadPDF() {
    const file = document.getElementById("pdfFile").files[0];

    if (!file) {
        alert("Please upload a PDF");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    extractedText = data.text;

    document.getElementById("textOutput").value = extractedText;
}


// Summarize
async function summarizeText() {
    if (!extractedText) {
        alert("Upload PDF first");
        return;
    }

    const response = await fetch(`${API_URL}/summarize`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: extractedText })
    });

    const data = await response.json();

    document.getElementById("resultBox").innerText = data.summary;
}


// Generate Quiz
async function generateQuiz() {
    if (!extractedText) {
        alert("Upload PDF first");
        return;
    }

    const response = await fetch(`${API_URL}/quiz`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: extractedText })
    });

    const data = await response.json();

    document.getElementById("resultBox").innerText =
        data.quiz.join("\n");
}