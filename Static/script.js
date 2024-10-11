document.getElementById('emailForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const emailText = document.getElementById('email_text').value;

    // Enviar los datos a la API usando fetch
    fetch('/analyze-email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email_text: emailText })
    })
    .then(response => response.json())
    .then(data => {
        // Mostrar el resultado en la página
        const resultDiv = document.getElementById('result');
        if (data.error) {
            resultDiv.textContent = `Error: ${data.error}`;
        } else {
            resultDiv.textContent = `Resultado: ${data.result}`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
