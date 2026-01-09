async function createIssue(event) {
    event.preventDefault();

    const issueData = {
        title: document.getElementById("title").value,
        category: document.getElementById("category").value,
        location: document.getElementById("location").value,
        description: document.getElementById("description").value
    };

    const response = await fetch(`${API_BASE_URL}/issues`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${getToken()}`
        },
        body: JSON.stringify(issueData)
    });

    if (response.ok) {
        alert("Issue submitted successfully");
        loadIssues();
        event.target.reset(); // clears form
    }
}

async function loadIssues() {
    const response = await fetch(`${API_BASE_URL}/issues/my`, {
        headers: {
            "Authorization": `Bearer ${getToken()}`
        }
    });

    const issues = await response.json();
    const list = document.getElementById("issuesList");
    list.innerHTML = "";

    if (issues.length === 0) {
        list.innerHTML = "<p>No issues reported yet.</p>";
        return;
    }

    issues.forEach(issue => {
        list.innerHTML += `
            <div class="issue-item">
                <div class="issue-title">${issue.title}</div>
                <div class="issue-meta">
                    ${issue.category} • ${issue.location}
                </div>
                <span class="status ${issue.status.toLowerCase().replace(" ", "-")}">
                    ${issue.status}
                </span>
            </div>
        `;
    });
}

