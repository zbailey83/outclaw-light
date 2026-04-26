let tokenClient;
let accessToken = null;
const CLIENT_ID = '477890661542-9luu0td5glsfse8dh0qvsu3oos9leigj.apps.googleusercontent.com';
const GA_PROPERTY_ID = '529241982';

function connectGoogle() {
    tokenClient = google.accounts.oauth2.initTokenClient({
        client_id: CLIENT_ID,
        scope: 'https://www.googleapis.com/auth/analytics.readonly https://www.googleapis.com/auth/webmasters.readonly',
        callback: (response) => {
            if (response.access_token) {
                accessToken = response.access_token;
                document.getElementById('google-connect-btn').innerHTML = '<i data-lucide="check"></i><span>Google Connected</span>';
                lucide.createIcons();
                fetchRealData();
            }
        },
    });
    tokenClient.requestAccessToken();
}

async function fetchRealData() {
    console.log('Fetching real data with token:', accessToken);
    
    // Set loading states
    document.getElementById('val-users').innerText = '...';
    document.getElementById('val-clicks').innerText = '...';
    
    try {
        // 1. Fetch GA4 Data (Active Users - Last 30 Days)
        if (GA_PROPERTY_ID !== 'YOUR_GA4_PROPERTY_ID') {
            const gaResponse = await fetch(`https://analyticsdata.googleapis.com/v1beta/properties/${GA_PROPERTY_ID}:runReport`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
                    metrics: [{ name: 'activeUsers' }, { name: 'sessions' }]
                })
            });
            const gaData = await gaResponse.json();
            if (gaData.rows) {
                document.getElementById('val-users').innerText = parseInt(gaData.rows[0].metricValues[0].value).toLocaleString();
            }
        }

        // 2. Fetch GSC Data (Clicks/Impressions - Last 30 Days)
        const gscResponse = await fetch(`https://www.googleapis.com/webmasters/v3/sites/https%3A%2F%2Foutclaw.xyz/searchAnalytics/query`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                startDate: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
                endDate: new Date().toISOString().split('T')[0],
                dimensions: ['query'],
                rowLimit: 5
            })
        });
        const gscData = await gscResponse.json();
        if (gscData.rows) {
            let totalClicks = gscData.rows.reduce((acc, row) => acc + row.clicks, 0);
            document.getElementById('val-clicks').innerText = totalClicks.toLocaleString();
            renderQueries(gscData.rows);
        }

        showSuccessToast('Dashboard synced with live Google data!');
    } catch (err) {
        console.error('API Error:', err);
        showSuccessToast('Connected, but failed to fetch data. Check permissions.');
    }
}

function showSuccessToast(msg) {
    const toast = document.createElement('div');
    toast.style.cssText = 'position:fixed; bottom:20px; right:20px; background:var(--sky); color:white; padding:12px 24px; border-radius:12px; z-index:1000; animation: fadeInUp 0.3s ease';
    toast.innerText = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function checkAuth() {
    const input = document.getElementById('access-key').value;
    const error = document.getElementById('auth-error');
    
    if (input === SECRET_KEY) {
        document.getElementById('auth-gate').style.opacity = '0';
        setTimeout(() => {
            document.getElementById('auth-gate').style.display = 'none';
            document.getElementById('dashboard-content').style.display = 'flex';
            initCharts();
            renderQueries();
        }, 500);
        localStorage.setItem('outclaw_admin_auth', 'true');
    } else {
        error.style.display = 'block';
    }
}

function logout() {
    localStorage.removeItem('outclaw_admin_auth');
    location.reload();
}

// Auto-login if already authenticated
window.onload = () => {
    if (localStorage.getItem('outclaw_admin_auth') === 'true') {
        document.getElementById('auth-gate').style.display = 'none';
        document.getElementById('dashboard-content').style.display = 'flex';
        initCharts();
        renderQueries();
    }
};

function initCharts() {
    // Traffic Chart (Line)
    const trafficCtx = document.getElementById('trafficChart').getContext('2d');
    new Chart(trafficCtx, {
        type: 'line',
        data: {
            labels: ['Apr 1', 'Apr 5', 'Apr 10', 'Apr 15', 'Apr 20', 'Apr 25'],
            datasets: [{
                label: 'Daily Users',
                data: [120, 190, 150, 280, 240, 310],
                borderColor: '#5AADDB',
                backgroundColor: 'rgba(90, 173, 219, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: '#fff',
                pointBorderColor: '#5AADDB',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { display: false } },
                x: { grid: { display: false } }
            }
        }
    });

    // Sources Chart (Doughnut)
    const sourceCtx = document.getElementById('sourceChart').getContext('2d');
    new Chart(sourceCtx, {
        type: 'doughnut',
        data: {
            labels: ['Direct', 'Organic Search', 'Social', 'Referral'],
            datasets: [{
                data: [45, 30, 15, 10],
                backgroundColor: ['#5AADDB', '#F4678A', '#FF7E5A', '#B8DFF0'],
                borderWidth: 0,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { boxWidth: 12, padding: 20, font: { family: 'DM Sans' } }
                }
            },
            cutout: '70%'
        }
    });

    // Position Chart (Bar)
    const posCtx = document.getElementById('positionChart').getContext('2d');
    new Chart(posCtx, {
        type: 'bar',
        data: {
            labels: ['M', 'T', 'W', 'T', 'F', 'S', 'S'],
            datasets: [{
                label: 'Avg Position',
                data: [12.4, 11.8, 11.2, 12.1, 10.5, 9.8, 10.2],
                backgroundColor: '#F4678A',
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { reverse: true, grid: { display: false } },
                x: { grid: { display: false } }
            }
        }
    });
}

function renderQueries(realData = null) {
    const defaultQueries = [
        { term: 'ai newsletter for builders', clicks: 142, pos: 1.2 },
        { term: 'mcp practical guide', clicks: 84, pos: 2.4 },
        { term: 'prompt frameworks 2026', clicks: 56, pos: 4.1 },
        { term: 'outclaw ai', clicks: 42, pos: 1.0 },
        { term: 'best ai workflows', clicks: 31, pos: 8.3 }
    ];

    const data = realData ? realData.map(r => ({ term: r.keys[0], clicks: r.clicks, pos: r.position.toFixed(1) })) : defaultQueries;

    const container = document.getElementById('top-queries');
    container.innerHTML = data.map(q => `
        <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #F1F5F9;">
            <div style="font-size: 14px; font-weight: 500;">${q.term}</div>
            <div style="display: flex; gap: 20px; font-size: 13px; color: var(--text-soft);">
                <span>${q.clicks} clicks</span>
                <span style="color: var(--sky);">Pos: ${q.pos}</span>
            </div>
        </div>
    `).join('');
}

// Simulating Live Data Updates
setInterval(() => {
    if (document.getElementById('dashboard-content').style.display === 'flex') {
        // Update Users
        const usersEl = document.getElementById('val-users');
        let users = parseInt(usersEl.innerText.replace(',', ''));
        users += Math.random() > 0.7 ? 1 : 0;
        usersEl.innerText = users.toLocaleString();

        // Update Subs (randomly add a new subscriber every now and then)
        const subsEl = document.getElementById('val-subs');
        if (Math.random() > 0.95) {
            let subs = parseInt(subsEl.innerText.replace(',', ''));
            subs += 1;
            subsEl.innerText = subs.toLocaleString();
            
            // Notification effect
            subsEl.style.color = '#F4678A';
            setTimeout(() => subsEl.style.color = '', 2000);
        }
    }
}, 3000);
