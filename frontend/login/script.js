document.getElementById('login-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    const response = await fetch('http://localhost:8000/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
            'username': username,
            'password': password
        })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        const decodedToken = jwt_decode(data.access_token);

        if (decodedToken.role === 'admin') {
            window.location.href = '/admin/';
        } else if (decodedToken.role === 'waiter') {
            window.location.href = '/waiter/';
        } else if (decodedToken.role === 'kitchen') {
            window.location.href = '/kitchen/';
        }
    } else {
        errorMessage.textContent = 'Invalid username or password';
    }
});
