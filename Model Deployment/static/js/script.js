window.onload = function() {
    fetch('/get-dropdown-options')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            label_encoded_collumns.forEach(function(col) {
                var select = document.getElementById(col);
                data[col].forEach(function(option) {
                    var newOption = document.createElement('option');
                    newOption.value = option;
                    newOption.innerHTML = option;
                    select.appendChild(newOption);
                });
            });
        })
        .catch(error => console.error('Error:', error));
    };


document.getElementById('predictionForm').onsubmit = function(e) {
    e.preventDefault();

    var formData = {};
    input_collumns.forEach(function(col) {
        formData[col] = document.getElementById(col).value;
    });

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('predictionResult').innerHTML = 'Mức lương được dự đoán là: ' + data.prediction;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
};