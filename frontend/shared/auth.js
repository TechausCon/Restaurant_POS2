const apiUrl = 'http://localhost:8000';

function getToken() {
    return localStorage.getItem('token');
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/login/';
}

function checkAuth() {
    if (!getToken()) {
        window.location.href = '/login/';
    }
}

async function fetchWithAuth(url, options = {}) {
    const token = getToken();
    const headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`
    };
    const response = await fetch(`${apiUrl}${url}`, { ...options, headers });
    if (response.status === 401) {
        logout();
    }
    return response;
}
