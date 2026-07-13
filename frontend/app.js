document.addEventListener('DOMContentLoaded', () => {
    fetchIncidents();
    // Poll for new incidents every 5 seconds
    setInterval(fetchIncidents, 5000);
});

async function fetchIncidents() {
    try {
        const response = await fetch('/api/incidents');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        
        updateDashboard(data.incidents);
    } catch (error) {
        console.error('Failed to fetch incidents:', error);
        document.getElementById('incident-feed').innerHTML = '<div class="loading">Unable to connect to telemetry stream...</div>';
    }
}

function updateDashboard(incidents) {
    const feed = document.getElementById('incident-feed');
    const totalEl = document.getElementById('total-incidents');
    const prsEl = document.getElementById('active-prs');
    
    totalEl.textContent = incidents.length;
    prsEl.textContent = incidents.filter(i => i.pr_url).length;

    if (incidents.length === 0) {
        feed.innerHTML = '<div class="loading">No recent incidents detected. System is stable.</div>';
        return;
    }

    feed.innerHTML = '';
    
    incidents.forEach(incident => {
        const date = new Date(incident.timestamp).toLocaleString();
        
        const item = document.createElement('div');
        item.className = 'incident-item';
        
        let prHtml = '';
        if (incident.pr_url) {
            prHtml = `<a href="${incident.pr_url}" target="_blank" class="pr-link">View Pull Request ↗</a>`;
        }

        item.innerHTML = `
            <div class="incident-info">
                <h4>${incident.app_name}</h4>
                <p>Time: ${date}</p>
                <span class="diagnostic-tag">${incident.diagnostic}</span>
            </div>
            <div class="incident-action">
                <div class="status-badge">${incident.status}</div>
                <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 0.5rem;">${incident.proposed_fix}</p>
                ${prHtml}
            </div>
        `;
        
        feed.appendChild(item);
    });
}
