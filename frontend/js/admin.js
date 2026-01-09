async function adminLogin(event) {
    event.preventDefault();
    const email = document.getElementById("adminEmail").value;
    const password = document.getElementById("adminPassword").value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (response.ok) {
            // Store token for later requests
            localStorage.setItem("token", data.access_token);
            window.location.href = "admin_dashboard.html"; // redirect to dashboard
        } else {
            alert(data.detail || "Login failed");
        }
    } catch (err) {
        console.error(err);
        alert("Login failed, check console");
    }
}
