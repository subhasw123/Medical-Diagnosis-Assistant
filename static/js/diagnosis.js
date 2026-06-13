let allSymptoms = [];
let selectedSymptoms = new Set();

document.addEventListener("DOMContentLoaded", function () {

    loadSymptoms();

    const searchInput =
        document.getElementById("symptom-search");

    if (searchInput) {
        searchInput.addEventListener(
            "input",
            function (e) {

                const query =
                    e.target.value.toLowerCase();

                const filtered =
                    allSymptoms.filter(symptom =>
                        symptom
                            .toLowerCase()
                            .includes(query)
                    );

                renderSymptomList(filtered);
            }
        );
    }

    const form =
        document.getElementById("diagnosis-form");

    if (form) {

        form.addEventListener(
            "submit",
            submitDiagnosis
        );
    }
});

async function loadSymptoms() {

    try {

        const response =
            await fetch(
                "/diagnosis/symptoms"
            );

        const data =
            await response.json();

        allSymptoms =
            data.symptoms || [];

        renderSymptomList(allSymptoms);

    } catch (error) {

        console.error(
            "Error loading symptoms:",
            error
        );
    }
}

async function submitDiagnosis(event) {

    event.preventDefault();

    if (selectedSymptoms.size === 0) {

        alert(
            "Please select at least one symptom."
        );

        return;
    }

    try {

        const form =
            document.getElementById(
                "diagnosis-form"
            );

        const formData =
            new FormData(form);

        const payload = {

            full_name:
                formData.get("full_name"),

            age:
                parseInt(
                    formData.get("age")
                ),

            gender:
                formData.get("gender"),

            symptoms:
                Array.from(
                    selectedSymptoms
                )
        };

        const response =
            await fetch(
                "/diagnosis/",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body: JSON.stringify(
                        payload
                    )
                }
            );

        const data =
            await response.json();

        console.log(
            "Prediction Response:",
            data
        );

        renderResults(data);

    } catch (error) {

        console.error(
            "Prediction Error:",
            error
        );

        alert(
            "Error occurred while predicting disease."
        );
    }
}

function renderResults(data) {

    const resultContainer =
        document.getElementById(
            "result-container"
        );

    if (!resultContainer) {

        console.error(
            "result-container not found."
        );

        return;
    }

    if (
        !data ||
        !data.predictions ||
        data.predictions.length === 0
    ) {

        resultContainer.innerHTML = `
            <div class="prediction-card">
                No predictions available.
            </div>
        `;

        return;
    }

    let html = `
        <h2 style="margin-top:30px;">
            Top 3 Disease Predictions
        </h2>
    `;

    data.predictions.forEach(
        (prediction, index) => {

            let adviceHTML = "";

            if (
                Array.isArray(
                    prediction.advice
                )
            ) {

                adviceHTML =
                    prediction.advice
                        .map(item =>
                            `<li>${item}</li>`
                        )
                        .join("");

            } else if (
                prediction.advice
            ) {

                adviceHTML =
                    `<li>${prediction.advice}</li>`;

            } else {

                adviceHTML =
                    `<li>No advice available</li>`;
            }

            html += `
                <div class="prediction-card">

                    <h3>
                        #${index + 1}
                        ${prediction.disease || "Unknown Disease"}
                    </h3>

                    <p>
                        <strong>
                            Relative Confidence:
                        </strong>
                        ${prediction.confidence || 0}%
                    </p>

                    <div class="progress">
                        <div
                            class="progress-bar"
                            style="
                                width:
                                ${prediction.confidence || 0}%;
                            "
                        >
                            ${prediction.confidence || 0}%
                        </div>
                    </div>

                    <p>
                        <strong>
                            Model Probability:
                        </strong>
                        ${prediction.raw_probability || 0}%
                    </p>

                    <p>
                        <strong>
                            Description:
                        </strong>
                        <br>
                        ${prediction.description || "No description available"}
                    </p>

                    <p>
                        <strong>
                            Advice:
                        </strong>
                    </p>

                    <ul>
                        ${adviceHTML}
                    </ul>

                </div>
            `;
        }
    );

    resultContainer.innerHTML =
        html;

    resultContainer.scrollIntoView({
        behavior: "smooth"
    });
}

function renderSymptomList(symptoms) {

    const symptomList =
        document.getElementById(
            "symptom-list"
        );

    if (!symptomList) return;

    if (symptoms.length === 0) {

        symptomList.innerHTML =
            `<div class="no-results">
                No symptoms found
            </div>`;

        return;
    }

    symptomList.innerHTML =
        symptoms
            .map(symptom => `
                <div class="symptom-item">

                    <input
                        type="checkbox"
                        id="symptom-${symptom}"
                        value="${symptom}"
                        ${
                            selectedSymptoms.has(symptom)
                                ? "checked"
                                : ""
                        }
                    >

                    <label
                        for="symptom-${symptom}"
                    >
                        ${symptom}
                    </label>

                </div>
            `)
            .join("");

    document
        .querySelectorAll(
            '.symptom-item input[type="checkbox"]'
        )
        .forEach(checkbox => {

            checkbox.addEventListener(
                "change",
                function () {

                    if (this.checked) {

                        selectedSymptoms.add(
                            this.value
                        );

                    } else {

                        selectedSymptoms.delete(
                            this.value
                        );
                    }

                    updateSelectedSymptomsDisplay();
                }
            );
        });
}

function updateSelectedSymptomsDisplay() {

    const container =
        document.getElementById(
            "selected-symptoms"
        );

    const input =
        document.getElementById(
            "symptoms-input"
        );

    if (!container || !input) return;

    if (selectedSymptoms.size === 0) {

        container.innerHTML =
            `<span style="color:#999;">
                No symptoms selected
            </span>`;

        input.value = "";

        return;
    }

    container.innerHTML =
        Array.from(
            selectedSymptoms
        )
            .map(symptom => `
                <div class="symptom-tag">

                    ${symptom}

                    <button
                        type="button"
                        onclick="removeSymptom('${symptom}')"
                    >
                        ×
                    </button>

                </div>
            `)
            .join("");

    input.value =
        Array.from(
            selectedSymptoms
        ).join(",");
}

function removeSymptom(symptom) {

    selectedSymptoms.delete(symptom);

    const checkbox =
        document.getElementById(
            `symptom-${symptom}`
        );

    if (checkbox) {

        checkbox.checked = false;
    }

    updateSelectedSymptomsDisplay();
}

async function sendMessage() {

    const input =
        document.getElementById(
            "chat-input"
        );

    const chatBox =
        document.getElementById(
            "chat-box"
        );

    if (!input || !chatBox) return;

    const question =
        input.value.trim();

    if (!question) return;

    chatBox.innerHTML += `
        <div>
            <b>You:</b>
            ${question}
        </div>
    `;

    input.value = "";

    try {

        const response =
            await fetch(
                "/chatbot/ask",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body: JSON.stringify({
                        question: question
                    })
                }
            );

        const data =
            await response.json();

        chatBox.innerHTML += `
            <div style="margin-top:10px;">
                <b>AI:</b>
                ${data.answer || "No response"}
            </div>
            <hr>
        `;

    } catch (error) {

        console.error(error);

        chatBox.innerHTML += `
            <div>
                <b>AI:</b>
                Error getting response.
            </div>
            <hr>
        `;
    }

    chatBox.scrollTop =
        chatBox.scrollHeight;
}