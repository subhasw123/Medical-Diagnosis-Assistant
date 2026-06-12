let allSymptoms = [];
let selectedSymptoms = new Set();

document.addEventListener('DOMContentLoaded', function () {

    // Load symptoms
    fetch('/diagnosis/symptoms')
        .then(response => response.json())
        .then(data => {
            allSymptoms = data.symptoms;
            renderSymptomList(allSymptoms);
        })
        .catch(error => {
            console.error('Error loading symptoms:', error);
        });

    // Search symptoms
    const searchInput = document.getElementById('symptom-search');

    if (searchInput) {
        searchInput.addEventListener('input', function (e) {

            const query = e.target.value.toLowerCase();

            const filteredSymptoms = allSymptoms.filter(symptom =>
                symptom.toLowerCase().includes(query)
            );

            renderSymptomList(filteredSymptoms);
        });
    }

    // Form submit
    const form = document.getElementById('diagnosis-form');

    if (form) {

        form.addEventListener('submit', function (event) {

            event.preventDefault();

            const formData = new FormData(form);

            const payload = {
                full_name: formData.get('full_name'),
                age: parseInt(formData.get('age')),
                gender: formData.get('gender'),
                symptoms: Array.from(selectedSymptoms)
            };

            if (selectedSymptoms.size === 0) {
                alert('Please select at least one symptom.');
                return;
            }

            fetch('/diagnosis/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            })
                .then(response => response.json())
                .then(data => {

                    const resultContainer =
                        document.getElementById('result-container');

                    let html = `
                        <h2 style="margin-top:30px;">
                            Top 3 Disease Predictions
                        </h2>
                    `;

                    data.predictions.forEach((prediction, index) => {

                        html += `
                            <div class="prediction-card">

                                <h3>
                                    #${index + 1}
                                    ${prediction.disease}
                                </h3>

                                <p>
                                    <strong>Relative Confidence:</strong>
                                    ${prediction.confidence}%
                                </p>

                                <div class="progress">
                                    <div
                                        class="progress-bar"
                                        style="width:${prediction.confidence}%"
                                    >
                                        ${prediction.confidence}%
                                    </div>
                                </div>

                                <p>
                                    <strong>Model Probability:</strong>
                                    ${prediction.raw_probability}%
                                </p>

                                <p>
                                    <strong>Description:</strong><br>
                                    ${prediction.description}
                                </p>

                                <p>
                                    <strong>Advice:</strong>
                                </p>

                                <ul>
                                    ${prediction.advice
                                        .map(item => `<li>${item}</li>`)
                                        .join('')}
                                </ul>

                            </div>
                        `;
                    });

                    resultContainer.innerHTML = html;

                    resultContainer.scrollIntoView({
                        behavior: "smooth"
                    });

                })
                .catch(error => {

                    console.error(error);

                    alert(
                        'Error occurred while predicting disease.'
                    );
                });
        });
    }
});

function renderSymptomList(symptoms) {

    const symptomList =
        document.getElementById('symptom-list');

    if (!symptomList) return;

    if (symptoms.length === 0) {

        symptomList.innerHTML =
            '<div class="no-results">No symptoms found</div>';

        return;
    }

    symptomList.innerHTML = symptoms
        .map(symptom => `
            <div class="symptom-item">

                <input
                    type="checkbox"
                    id="symptom-${symptom}"
                    value="${symptom}"
                    ${selectedSymptoms.has(symptom) ? 'checked' : ''}
                >

                <label for="symptom-${symptom}">
                    ${symptom}
                </label>

            </div>
        `)
        .join('');

    document
        .querySelectorAll(
            '.symptom-item input[type="checkbox"]'
        )
        .forEach(checkbox => {

            checkbox.addEventListener(
                'change',
                function () {

                    if (this.checked) {
                        selectedSymptoms.add(this.value);
                    } else {
                        selectedSymptoms.delete(this.value);
                    }

                    updateSelectedSymptomsDisplay();
                }
            );
        });
}

function updateSelectedSymptomsDisplay() {

    const selectedSymptomsDiv =
        document.getElementById(
            'selected-symptoms'
        );

    const symptomsInput =
        document.getElementById(
            'symptoms-input'
        );

    if (selectedSymptoms.size === 0) {

        selectedSymptomsDiv.innerHTML =
            '<span style="color:#999;">No symptoms selected</span>';

        symptomsInput.value = '';

        return;
    }

    selectedSymptomsDiv.innerHTML =
        Array.from(selectedSymptoms)
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
            .join('');

    symptomsInput.value =
        Array.from(selectedSymptoms).join(',');
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