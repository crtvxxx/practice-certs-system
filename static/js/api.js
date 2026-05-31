const BASE_URL = ''; 

async function apiRequest(endpoint, method = 'GET', body = null) {
    const token = localStorage.getItem('access_token');
    const headers = {
        'Content-Type': 'application/json',
    };
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        method,
        headers,
    };
    if (body && method !== 'GET') {
        config.body = JSON.stringify(body);
    }

    const response = await fetch(BASE_URL + endpoint, config);
    const data = await response.json();

    if (!response.ok) {
        const error = new Error(data.detail || 'Ошибка запроса');
        error.status = response.status;
        throw error;
    }
    return data;
}