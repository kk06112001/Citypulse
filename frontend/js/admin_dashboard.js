// =================== admin_dashboard.js ===================

// Store issues globally for stats & charts
let allIssues = [];
let issuesChart = null;

// Get JWT token
function getToken() {
    return localStorage.getItem("token");
}

// Load all issues and populate table
async function loadAllIssues() {
    const token = getToken();
    if (!token) { 
        alert("Login required"); 
        window.location.href = "admin.html"; 
        return; 
    }

    try {
        const response = await fetch(`${API_BASE_URL}/admin/issues`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (!response.ok) {
            const data = await response.json();
            alert(data.detail || "Failed to fetch issues.");
            return;
        }

        allIssues = await response.json();

        renderTable(allIssues);
        updateStats(allIssues);
        renderChart(allIssues);

    } catch (err) {
        console.error("Error loading issues:", err);
        alert("Something went wrong while fetching issues.");
    }
}

// ================= TABLE RENDER =================
function renderTable(issues) {
    const table = document.getElementById("issuesTable");
    table.innerHTML = "";

    issues.forEach(issue => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${issue.id}</td>
            <td>${issue.title}</td>
            <td>${issue.citizen_email || issue.citizen_id}</td>
            <td>
                <span class="status ${issue.status.toLowerCase().replace(" ", "-")}">
                    ${issue.status}
                </span>
            </td>
            <td>${issue.assigned_to || "-"}</td>
            <td>
                <input type="text" placeholder="Assign to" id="assign_${issue.id}">
                <button class="action-btn assign-btn" onclick="assignIssue(${issue.id})">
                    Assign
                </button>

                <select id="status_${issue.id}">
                    <option value="Open" ${issue.status === "Open" ? "selected" : ""}>Open</option>
                    <option value="In Progress" ${issue.status === "In Progress" ? "selected" : ""}>In Progress</option>
                    <option value="Resolved" ${issue.status === "Resolved" ? "selected" : ""}>Resolved</option>
                </select>

                <button class="action-btn resolve-btn" onclick="updateStatus(${issue.id})">
                    Update
                </button>
            </td>
        `;
        table.appendChild(tr);
    });
}

// ================= STATS =================
function updateStats(issues) {
    document.getElementById("totalIssues").textContent = issues.length;

    document.getElementById("pendingIssues").textContent =
        issues.filter(i => i.status === "Open" || i.status === "Pending").length;

    document.getElementById("inProgressIssues").textContent =
        issues.filter(i => i.status === "In Progress").length;

    document.getElementById("resolvedIssues").textContent =
        issues.filter(i => i.status === "Resolved").length;
}

// ================= CHART =================
function renderChart(issues) {
    const pending = issues.filter(i => i.status === "Open" || i.status === "Pending").length;
    const progress = issues.filter(i => i.status === "In Progress").length;
    const resolved = issues.filter(i => i.status === "Resolved").length;

    const ctx = document.getElementById("issuesChart").getContext("2d");

    // Destroy previous chart if exists
    if (issuesChart) {
        issuesChart.destroy();
    }

    issuesChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: ["Pending", "In Progress", "Resolved"],
            datasets: [{
                data: [pending, progress, resolved],
                backgroundColor: [
                    "#ffeeba",   // Pending
                    "#cce5ff",   // In Progress
                    "#d4edda"    // Resolved
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,   // 🔑 important
            radius: "70%", 
            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });
}


// ================= ASSIGN ISSUE =================
async function assignIssue(issueId) {
    const assignedTo = document.getElementById(`assign_${issueId}`).value.trim();
    if (!assignedTo) {
        alert("Please enter a staff name.");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/admin/issues/${issueId}/assign`, {
            method: "PUT",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getToken()}`
            },
            body: JSON.stringify({ assigned_to: assignedTo })
        });

        const data = await response.json();
        if (response.ok) {
            alert("Assigned successfully");
            loadAllIssues();
        } else {
            alert(data.detail || "Assign failed");
        }

    } catch (err) {
        console.error(err);
        alert("Failed to assign issue.");
    }
}

// ================= UPDATE STATUS =================
async function updateStatus(issueId) {
    const status = document.getElementById(`status_${issueId}`).value;

    try {
        const response = await fetch(`${API_BASE_URL}/admin/issues/${issueId}/status`, {
            method: "PATCH",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getToken()}`
            },
            body: JSON.stringify({ status })
        });

        const data = await response.json();
        if (response.ok) {
            alert(`Status updated to ${status}`);
            loadAllIssues();
        } else {
            alert(data.detail || "Update failed");
        }

    } catch (err) {
        console.error(err);
        alert("Failed to update issue status.");
    }
}
// ================= EXPORT TO CSV =================
function exportToCSV() {
    if (!allIssues || allIssues.length === 0) {
        alert("No issues to export.");
        return;
    }

    const headers = ["ID", "Title", "Citizen", "Status", "Assigned To"];
    const rows = allIssues.map(issue => [
        issue.id,
        issue.title,
        issue.citizen_email || issue.citizen_id,
        issue.status,
        issue.assigned_to || "-"
    ]);

    // Combine headers and rows
    const csvContent = [headers, ...rows]
        .map(e => e.map(v => `"${v}"`).join(",")) // Wrap each value in quotes
        .join("\n");

    // Create a Blob and download
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = `citypulse_issues_${new Date().toISOString().slice(0,10)}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}
document.getElementById("exportBtn").addEventListener("click", exportToCSV);

// Auto-load
window.onload = loadAllIssues;
