document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let name = document.getElementById('name').value;
    let email = document.getElementById('email').value;
    let isAdmin = document.getElementById('is_admin').checked;

    let formData = new FormData();
    formData.append('name', name);
    formData.append('email', email);
    formData.append('isAdmin', isAdmin);

    if (name && email) {
        fetch('http://localhost:8000/register/', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('Registration successful!');
        })
        .catch((error) => {
            console.error('Error:', error);
            messageDiv.textContent = 'An error occurred. Please try again.';
        });
    } else {
        messageDiv.textContent = 'Please fill out all required fields.';
    }
});
