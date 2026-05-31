function logout() {
    localStorage.removeItem('access_token');
    window.location.replace('/static/login.html');
}