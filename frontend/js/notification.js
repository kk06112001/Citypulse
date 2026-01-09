async function loadNotifications() {
    // 1️⃣ Get all issues
    const response = await fetch(`${API_BASE_URL}/issues/my`, {
        headers: {
            "Authorization": `Bearer ${getToken()}`
        }
    });
    const issues = await response.json();

    const list = document.getElementById("notificationsList");
    list.innerHTML = "";

    // 2️⃣ Get previously stored statuses
    const previousStatuses = JSON.parse(localStorage.getItem("issueStatuses") || "{}");

    let hasNotification = false;

    issues.forEach(issue => {
        const oldStatus = previousStatuses[issue.id]; // undefined on first load
        const newStatus = issue.status;

        // 3️⃣ Compare old vs new
        if (oldStatus && oldStatus !== newStatus) {
            const li = document.createElement("li");
            li.textContent = `🔔 Status of "${issue.title}" changed from ${oldStatus} → ${newStatus}`;
            list.appendChild(li);
            hasNotification = true;
        }

        // 4️⃣ Update localStorage with current status
        previousStatuses[issue.id] = newStatus;
    });

    localStorage.setItem("issueStatuses", JSON.stringify(previousStatuses));

    if (!hasNotification) {
        list.innerHTML = "<li>No new notifications.</li>";
    }
}
