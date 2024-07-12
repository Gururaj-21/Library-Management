document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let mail_id = document.getElementById('mail_id').value;
    let password = document.getElementById('password').value;

    // Perform basic validation
    if (mail_id.trim() === '') {
        alert('Please enter your email.');
        return;
    }

    if (password.trim() === '') {
        alert('Please enter your password.');
        return;
    }

    // Prepare the data to be sent
    let login_formData = new FormData();
    login_formData.append('mail_id', mail_id);
    login_formData.append('password', password);

    // Make an AJAX request to Django REST API
    fetch('http://localhost:8000/login_user/', {
        method: 'POST',
        body: login_formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Login successful:', data);
        // Optionally, redirect or perform other actions upon successful login
        // Example: Redirect to a different page
        window.location.href = '/Library_Management_App/templates/home.html';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Login failed. Please try again.');
    });
});
