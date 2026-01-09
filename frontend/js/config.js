const API_BASE_URL = "http://localhost:8000";

function getToken() {
    return localStorage.getItem("access_token");
}

function setToken(token) {
    localStorage.setItem("access_token", token);
}

function logout() {
    localStorage.clear();
    window.location.href = "index.html";
}
