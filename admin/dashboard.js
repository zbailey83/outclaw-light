let tokenClient;
let accessToken = null;
const CLIENT_ID = '875855106263-hgs5ntpgkoceh6eo0alaiheagn33vlqj.apps.googleusercontent.com';
const GA_PROPERTY_ID = '529241982';
const SECRET_KEY = 'outclaw2026';

function connectGoogle() {
    // Show the Google account selection modal
    const modal = document.getElementById('google-auth-modal');
    if (modal) {
        modal.style.display = 'flex';
        lucide.createIcons();
    }
}

function initiateRealOAuth() {
    const modal = document.getElementById('google-auth-modal');
    if (modal) {
        modal.style.display = 'none';
    }
    
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

function selectMockAccount(email) {
    const modal = document.getElementById('google-auth-modal');
    if (modal) {
        modal.style.display = 'none';
    }
    
    let displayEmail = email;
    if (email === 'new') {
        const userEmail = prompt("Enter your Google Account email:", "zbailey83@gmail.com");
        if (userEmail) displayEmail = userEmail;
        else displayEmail = "zbailey83@gmail.com";
    }
    
    // Set connected button state
    document.getElementById('google-connect-btn').innerHTML = `<i data-lucide="check"></i><span>Connected: ${displayEmail}</span>`;
    lucide.createIcons();
    
    fetchSimulatedData();
}

async function fetchSimulatedData() {
    console.log('Fetching simulated dashboard data...');
    
    // Set loading states
    document.getElementById('val-users').innerText = '...';
    document.getElementById('val-clicks').innerText = '...';
    document.getElementById('val-impressions').innerText = '...';
    
    // Wait for 1.2s to simulate API response latency
    await new Promise(resolve => setTimeout(resolve, 1200));
    
    const activeUsers = 3842;
    const searchClicks = 1290;
    const impressions = 68432;
    
    document.getElementById('val-users').innerText = activeUsers.toLocaleString();
    document.getElementById('val-clicks').innerText = searchClicks.toLocaleString();
    document.getElementById('val-impressions').innerText = impressions.toLocaleString();
    
    // Generate realistic simulated daily active users over last 30 days
    const dailyUsersRows = [];
    for (let i = 29; i >= 0; i--) {
        const d = new Date(Date.now() - i * 24 * 60 * 60 * 1000);
        // Create an upward trend with some weekday/weekend variation
        const dayOfWeek = d.getDay();
        const base = 100 + (30 - i) * 3; // base growth
        const weekendDrop = (dayOfWeek === 0 || dayOfWeek === 6) ? 0.7 : 1.0;
        const randomVariation = Math.random() * 30 - 15;
        const val = Math.round((base * weekendDrop) + randomVariation + 150);
        dailyUsersRows.push({
            dimensionValues: [{ value: d.toISOString().replace(/-/g, '').split('T')[0] }],
            metricValues: [{ value: val.toString() }]
        });
    }
    updateTrafficChart(dailyUsersRows);
    
    // Generate realistic simulated session sources
    const sourcesRows = [
        { dimensionValues: [{ value: 'Organic Search' }], metricValues: [{ value: '1840' }] },
        { dimensionValues: [{ value: 'Direct' }], metricValues: [{ value: '1210' }] },
        { dimensionValues: [{ value: 'Social' }], metricValues: [{ value: '540' }] },
        { dimensionValues: [{ value: 'Referral' }], metricValues: [{ value: '252' }] }
    ];
    updateSourceChart(sourcesRows);
    
    // Generate realistic simulated GSC daily average position over last 7 days
    const positionRows = [];
    for (let i = 6; i >= 0; i--) {
        const d = new Date(Date.now() - i * 24 * 60 * 60 * 1000);
        const dateStr = d.toISOString().split('T')[0];
        // Position improving slightly over time (lower number is better position)
        const pos = 12.5 - (6 - i) * 0.4 + (Math.random() * 1.2 - 0.6);
        positionRows.push({
            keys: [dateStr],
            position: pos
        });
    }
    updatePositionChart(positionRows);
    
    // Generate realistic top search queries
    const mockQueries = [
        { keys: ['ai newsletter for builders'], clicks: 142, position: 1.2 },
        { keys: ['mcp practical guide'], clicks: 84, position: 2.4 },
        { keys: ['prompt frameworks 2026'], clicks: 56, position: 4.1 },
        { keys: ['outclaw ai'], clicks: 42, position: 1.0 },
        { keys: ['best ai workflows'], clicks: 31, position: 8.3 }
    ];
    renderQueries(mockQueries);
    
    showSuccessToast('Dashboard synced with simulated Google data!');
}

async function fetchRealData() {
    console.log('Fetching real data with token:', accessToken);
    
    // Set loading states
    document.getElementById('val-users').innerText = '...';
    document.getElementById('val-clicks').innerText = '...';
    document.getElementById('val-impressions').innerText = '...';
    
    try {
        // --- 1. Dynamic Google Search Console (GSC) Site Detection ---
        let targetSiteUrl = 'sc-domain:outclaw.xyz'; // Default fallback
        try {
            const sitesResponse = await fetch('https://www.googleapis.com/webmasters/v3/sites', {
                headers: { 'Authorization': `Bearer ${accessToken}` }
            });
            const sitesData = await sitesResponse.json();
            console.log('User GSC sites:', sitesData);
            if (sitesData.siteEntry && sitesData.siteEntry.length > 0) {
                // Find a site that matches 'outclaw.xyz'
                const matchedSite = sitesData.siteEntry.find(site => site.siteUrl.includes('outclaw.xyz'));
                if (matchedSite) {
                    targetSiteUrl = matchedSite.siteUrl;
                    console.log('Found matching GSC site property:', targetSiteUrl);
                } else {
                    console.warn('No exact GSC property matching outclaw.xyz found. Using default:', targetSiteUrl);
                }
            }
        } catch (err) {
            console.error('Failed to list GSC sites, using default fallback:', err);
        }
        const encodedSiteUrl = encodeURIComponent(targetSiteUrl);

        // --- 2. Fetch GSC Overall Totals (Clicks & Impressions - Last 30 Days) ---
        try {
            const gscTotalsResponse = await fetch(`https://www.googleapis.com/webmasters/v3/sites/${encodedSiteUrl}/searchAnalytics/query`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    startDate: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
                    endDate: new Date().toISOString().split('T')[0]
                })
            });
            const gscTotalsData = await gscTotalsResponse.json();
            console.log('GSC Totals Data:', gscTotalsData);
            if (gscTotalsData.rows && gscTotalsData.rows.length > 0) {
                const totalClicks = gscTotalsData.rows[0].clicks;
                const totalImpressions = gscTotalsData.rows[0].impressions;
                document.getElementById('val-clicks').innerText = totalClicks.toLocaleString();
                document.getElementById('val-impressions').innerText = totalImpressions.toLocaleString();
            } else {
                document.getElementById('val-clicks').innerText = '0';
                document.getElementById('val-impressions').innerText = '0';
            }
        } catch (err) {
            console.error('Error fetching GSC totals:', err);
            document.getElementById('val-clicks').innerText = 'Error';
            document.getElementById('val-impressions').innerText = 'Error';
        }

        // --- 3. Fetch GSC Top 5 Search Queries ---
        try {
            const gscQueriesResponse = await fetch(`https://www.googleapis.com/webmasters/v3/sites/${encodedSiteUrl}/searchAnalytics/query`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    startDate: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
                    endDate: new Date().toISOString().split('T')[0],
                    dimensions: ['query'],
                    rowLimit: 5
                })
            });
            const gscQueriesData = await gscQueriesResponse.json();
            console.log('GSC Queries Data:', gscQueriesData);
            if (gscQueriesData.rows) {
                renderQueries(gscQueriesData.rows);
            } else {
                renderQueries([]);
            }
        } catch (err) {
            console.error('Error fetching GSC top queries:', err);
            renderQueries([]);
        }

        // --- 4. Fetch GSC Daily Average Positions (Last 7 Days) for Position Chart ---
        try {
            const gscDailyResponse = await fetch(`https://www.googleapis.com/webmasters/v3/sites/${encodedSiteUrl}/searchAnalytics/query`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    startDate: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
                    endDate: new Date().toISOString().split('T')[0],
                    dimensions: ['date']
                })
            });
            const gscDailyData = await gscDailyResponse.json();
            console.log('GSC Daily Data:', gscDailyData);
            if (gscDailyData.rows && gscDailyData.rows.length > 0) {
                // Sort by date ascending
                const sortedRows = gscDailyData.rows.sort((a, b) => a.keys[0].localeCompare(b.keys[0]));
                updatePositionChart(sortedRows);
            }
        } catch (err) {
            console.error('Error fetching GSC daily positions:', err);
        }

        // --- 5. Fetch GA4 Overall Active Users (Last 30 Days) ---
        if (GA_PROPERTY_ID !== 'YOUR_GA4_PROPERTY_ID') {
            try {
                const gaTotalsResponse = await fetch(`https://analyticsdata.googleapis.com/v1beta/properties/${GA_PROPERTY_ID}:runReport`, {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
                        metrics: [{ name: 'activeUsers' }]
                    })
                });
                const gaTotalsData = await gaTotalsResponse.json();
                console.log('GA4 Totals Data:', gaTotalsData);
                if (gaTotalsData.rows && gaTotalsData.rows.length > 0) {
                    const totalUsers = parseInt(gaTotalsData.rows[0].metricValues[0].value);
                    document.getElementById('val-users').innerText = totalUsers.toLocaleString();
                } else {
                    document.getElementById('val-users').innerText = '0';
                }
            } catch (err) {
                console.error('Error fetching GA4 totals:', err);
                document.getElementById('val-users').innerText = 'Error';
            }

            // --- 6. Fetch GA4 Daily Active Users (Last 30 Days) for Traffic Chart ---
            try {
                const gaDailyResponse = await fetch(`https://analyticsdata.googleapis.com/v1beta/properties/${GA_PROPERTY_ID}:runReport`, {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
                        metrics: [{ name: 'activeUsers' }],
                        dimensions: [{ name: 'date' }]
                    })
                });
                const gaDailyData = await gaDailyResponse.json();
                console.log('GA4 Daily Data:', gaDailyData);
                if (gaDailyData.rows && gaDailyData.rows.length > 0) {
                    const sortedRows = gaDailyData.rows.sort((a, b) => a.dimensionValues[0].value.localeCompare(b.dimensionValues[0].value));
                    updateTrafficChart(sortedRows);
                }
            } catch (err) {
                console.error('Error fetching GA4 daily active users:', err);
            }

            // --- 7. Fetch GA4 Session Sources (Last 30 Days) for Sources Chart ---
            try {
                const gaSourcesResponse = await fetch(`https://analyticsdata.googleapis.com/v1beta/properties/${GA_PROPERTY_ID}:runReport`, {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
                        metrics: [{ name: 'sessions' }],
                        dimensions: [{ name: 'sessionDefaultChannelGroup' }]
                    })
                });
                const gaSourcesData = await gaSourcesResponse.json();
                console.log('GA4 Sources Data:', gaSourcesData);
                if (gaSourcesData.rows && gaSourcesData.rows.length > 0) {
                    updateSourceChart(gaSourcesData.rows);
                }
            } catch (err) {
                console.error('Error fetching GA4 traffic sources:', err);
            }
        }

        showSuccessToast('Dashboard synced with live Google data!');
    } catch (err) {
        console.error('API Error:', err);
        showSuccessToast('Connected, but failed to fetch data. Check permissions.');
    }
}

function updateTrafficChart(rows) {
    const labels = rows.map(r => {
        const raw = r.dimensionValues[0].value; // YYYYMMDD
        const year = parseInt(raw.substring(0, 4));
        const month = parseInt(raw.substring(4, 6)) - 1;
        const day = parseInt(raw.substring(6, 8));
        const d = new Date(Date.UTC(year, month, day));
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', timeZone: 'UTC' });
    });
    const data = rows.map(r => parseInt(r.metricValues[0].value));
    
    if (window.trafficChartInstance) {
        window.trafficChartInstance.destroy();
    }
    
    const trafficCtx = document.getElementById('trafficChart').getContext('2d');
    window.trafficChartInstance = new Chart(trafficCtx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Daily Active Users',
                data: data,
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
}

function updateSourceChart(rows) {
    const labels = rows.map(r => r.dimensionValues[0].value);
    const data = rows.map(r => parseInt(r.metricValues[0].value));
    
    if (window.sourceChartInstance) {
        window.sourceChartInstance.destroy();
    }
    
    const palette = ['#5AADDB', '#F4678A', '#FF7E5A', '#B8DFF0', '#A3E2C9', '#FFE5A3'];
    const backgroundColors = labels.map((_, i) => palette[i % palette.length]);
    
    const sourceCtx = document.getElementById('sourceChart').getContext('2d');
    window.sourceChartInstance = new Chart(sourceCtx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors,
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
}

function updatePositionChart(rows) {
    const labels = rows.map(r => {
        const d = new Date(r.keys[0]);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', timeZone: 'UTC' });
    });
    const data = rows.map(r => parseFloat(r.position.toFixed(1)));
    
    if (window.positionChartInstance) {
        window.positionChartInstance.destroy();
    }
    
    const posCtx = document.getElementById('positionChart').getContext('2d');
    window.positionChartInstance = new Chart(posCtx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Avg Position',
                data: data,
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

function showSuccessToast(msg) {
    const toast = document.createElement('div');
    toast.style.cssText = 'position:fixed; bottom:20px; right:20px; background:var(--sky); color:white; padding:12px 24px; border-radius:12px; z-index:1000; animation: fadeInUp 0.3s ease';
    toast.innerText = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// Auto-login if already authenticated
window.onload = () => {
    initCharts();
    renderQueries();
};

function initCharts() {
    // Traffic Chart (Line)
    const trafficCtx = document.getElementById('trafficChart').getContext('2d');
    window.trafficChartInstance = new Chart(trafficCtx, {
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
    window.sourceChartInstance = new Chart(sourceCtx, {
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
    window.positionChartInstance = new Chart(posCtx, {
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
    if (document.getElementById('dashboard-content') && document.getElementById('dashboard-content').style.display !== 'none') {
        // Update Users
        const usersEl = document.getElementById('val-users');
        if (usersEl) {
            const usersText = usersEl.innerText.replace(/,/g, '');
            let users = parseInt(usersText);
            if (!isNaN(users)) {
                users += Math.random() > 0.7 ? 1 : 0;
                usersEl.innerText = users.toLocaleString();
            }
        }

        // Update Subs (randomly add a new subscriber every now and then)
        const subsEl = document.getElementById('val-subs');
        if (subsEl) {
            const subsText = subsEl.innerText.replace(/,/g, '');
            let subs = parseInt(subsText);
            if (!isNaN(subs)) {
                if (Math.random() > 0.95) {
                    subs += 1;
                    subsEl.innerText = subs.toLocaleString();
                    
                    // Notification effect
                    subsEl.style.color = '#F4678A';
                    setTimeout(() => subsEl.style.color = '', 2000);
                }
            }
        }
    }
}, 3000);
