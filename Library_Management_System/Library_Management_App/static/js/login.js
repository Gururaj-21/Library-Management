document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    const response = await fetch('http://127.0.0.1:8000/login_user/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
        const data = await response.json();
        // Redirect to home page
        window.location.href = data.redirect_url;
    } else {
        const errorData = await response.json();
        errorMessage.textContent = errorData.error || 'An error occurred';
    }
});
