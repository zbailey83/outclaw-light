const SECRET_KEY = 'outclaw2026';

// Supabase configuration - replace with real keys to pull actual data
const SUPABASE_URL = 'https://pjxoyoomnaglrzwdvelv.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBqeG95b29tbmFnbHJ6d2R2ZWx2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczMjEyMDgsImV4cCI6MjA5Mjg5NzIwOH0.75QblYTeXI7WAkiUSEFCwB3F0B2WCHs9QJe0v5PX4NY';

let supabase = null;
let leadActionsChart = null;
let discoveryPathsChart = null;

async function initSupabase() {
    // Wait for Supabase SDK to be available on window
    let attempts = 0;
    while (!window.supabase && attempts < 20) {
        await new Promise(resolve => setTimeout(resolve, 100));
        attempts++;
    }

    if (window.supabase) {
        try {
            supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
            console.log("Supabase initialized successfully");
        } catch (e) {
            console.error("Supabase client creation failed", e);
        }
    } else {
        console.warn("Supabase SDK not found after 2 seconds. Operating in mock mode.");
    }
    
    // Initial data load
    updateDateRange();
}

if (document.readyState === 'loading') {
    window.addEventListener('DOMContentLoaded', () => {
        initSupabase();
    });
} else {
    initSupabase();
}

async function updateDateRange() {
    const selector = document.getElementById('date-range-selector');
    if (!selector) return;
    
    const days = parseInt(selector.value);
    setLoadingState();
    
    try {
        const data = await fetchDashboardData(days);
        if (data) {
            renderDashboard(data);
        } else {
            showErrorState("No data returned");
        }
    } catch (error) {
        console.error("Error in updateDateRange:", error);
        showErrorState("Fetch failed");
    }
}

function showErrorState(msg) {
    const elements = ['val-sessions', 'val-visitors', 'val-leads', 'val-searches', 'val-impressions', 'val-search-conv'];
    elements.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerText = 'Error';
    });
    console.error("Dashboard error state:", msg);
}

function setLoadingState() {
    const values = ['val-sessions', 'val-visitors', 'val-leads', 'val-searches', 'val-impressions', 'val-search-conv'];
    const trends = ['trend-sessions', 'trend-visitors', 'trend-leads', 'trend-searches', 'trend-impressions'];
    
    values.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerText = '...';
    });
    
    trends.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerText = '...';
    });
}

async function fetchDashboardData(days) {
    console.log(`Fetching data for last ${days} days...`);
    if (!supabase) {
        console.warn('Supabase client not initialized or using mock mode.');
        return getMockData(days);
    }

    const startDate = new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString();

    try {
        console.log('Querying analytics_events table...');
        const { data: events, error } = await supabase
            .from('analytics_events')
            .select('*')
            .gte('created_at', startDate);

        if (error) {
            console.error('Supabase error:', error);
            throw error;
        }

        console.log(`Received ${events?.length || 0} events`);

        if (!events || events.length === 0) {
            console.warn('No events found in table. Returning empty totals.');
            return getEmptyData(days);
        }
            sessions: events.filter(e => e.event_type === 'session_start').length,
            visitors: new Set(events.map(e => e.session_id || Math.random())).size,
            leads: events.filter(e => e.event_type === 'lead_action').length,
            searches: events.filter(e => e.event_type === 'search').length,
            impressions: events.filter(e => e.event_type === 'impression').length,
            searchConv: events.filter(e => e.event_type === 'search').length > 0 
                ? ((events.filter(e => e.event_type === 'lead_action').length / events.filter(e => e.event_type === 'search').length) * 100).toFixed(1) + '%'
                : '0.0%'
        };

        // Lead Actions (Time series for bar chart)
        // Grouping by day
        const dailyData = {};
        for (let i = 0; i < days; i++) {
            const d = new Date(Date.now() - i * 24 * 60 * 60 * 1000).toLocaleDateString();
            dailyData[d] = { website: 0, directions: 0, phone: 0 };
        }

        events.filter(e => e.event_type === 'lead_action').forEach(e => {
            const d = new Date(e.created_at).toLocaleDateString();
            if (dailyData[d]) {
                const type = e.event_data?.type || 'website';
                if (dailyData[d][type] !== undefined) dailyData[d][type]++;
            }
        });

        const sortedDays = Object.keys(dailyData).reverse();

        return {
            totals,
            leadActions: {
                labels: sortedDays,
                website: sortedDays.map(d => dailyData[d].website),
                directions: sortedDays.map(d => dailyData[d].directions),
                phone: sortedDays.map(d => dailyData[d].phone)
            },
            discoveryPaths: [
                { name: 'Search', value: events.filter(e => e.source === 'search').length },
                { name: 'Browse', value: events.filter(e => e.source === 'browse').length },
                { name: 'Direct', value: events.filter(e => e.source === 'direct').length }
            ],
            topQueries: Object.entries(events.filter(e => e.event_type === 'search').reduce((acc, e) => {
                const q = e.event_data?.query || 'Unknown';
                acc[q] = (acc[q] || 0) + 1;
                return acc;
            }, {})).map(([term, clicks]) => ({ term, clicks })).sort((a, b) => b.clicks - a.clicks).slice(0, 5),
            zeroQueries: Object.entries(events.filter(e => e.event_type === 'search' && e.event_data?.results === 0).reduce((acc, e) => {
                const q = e.event_data?.query || 'Unknown';
                acc[q] = (acc[q] || 0) + 1;
                return acc;
            }, {})).map(([term, count]) => ({ term, count })).sort((a, b) => b.count - a.count).slice(0, 3),
            listingPerformance: Object.values(events.filter(e => e.center_name).reduce((acc, e) => {
                if (!acc[e.center_name]) acc[e.center_name] = { center: e.center_name, brand: e.brand, city: e.city, imp: 0, clicks: 0, leads: 0 };
                if (e.event_type === 'impression') acc[e.center_name].imp++;
                if (e.event_type === 'click') acc[e.center_name].clicks++;
                if (e.event_type === 'lead_action') acc[e.center_name].leads++;
                return acc;
            }, {})).map(item => ({
                ...item,
                rate: item.imp > 0 ? ((item.leads / item.imp) * 100).toFixed(1) + '%' : '0%'
            })).sort((a, b) => b.leads - a.leads).slice(0, 10)
        };
    } catch (err) {
        console.error('Supabase fetch error:', err);
        return getMockData(days);
    }
}

function getEmptyData(days) {
    return {
        totals: { sessions: 0, visitors: 0, leads: 0, searches: 0, impressions: 0, searchConv: '0.0%' },
        leadActions: { labels: [], website: [], directions: [], phone: [] },
        discoveryPaths: [
            { name: 'Search', value: 0 },
            { name: 'Browse', value: 0 },
            { name: 'Direct', value: 0 }
        ],
        topQueries: [],
        zeroQueries: [],
        listingPerformance: []
    };
}

// Fallback mock data function
function getMockData(days) {
    const multiplier = days === 7 ? 0.25 : (days === 90 ? 3 : 1);
    return {
        totals: {
            sessions: Math.floor(12450 * multiplier),
            visitors: Math.floor(8920 * multiplier),
            leads: Math.floor(843 * multiplier),
            searches: Math.floor(5200 * multiplier),
            impressions: Math.floor(45600 * multiplier),
            searchConv: (4.2).toFixed(1) + '%'
        },
        leadActions: {
            labels: Array.from({length: 7}, (_, i) => `Day ${i+1}`),
            directions: Array.from({length: 7}, () => Math.floor(Math.random() * 20 * multiplier)),
            website: Array.from({length: 7}, () => Math.floor(Math.random() * 50 * multiplier)),
            phone: Array.from({length: 7}, () => Math.floor(Math.random() * 15 * multiplier))
        },
        discoveryPaths: [
            { name: 'Search', value: Math.floor(65 * multiplier) },
            { name: 'Browse', value: Math.floor(25 * multiplier) },
            { name: 'Direct', value: Math.floor(10 * multiplier) }
        ],
        topQueries: [
            { term: 'ai automation agency', clicks: Math.floor(145 * multiplier) },
            { term: 'local marketing', clicks: Math.floor(84 * multiplier) },
            { term: 'outclaw pricing', clicks: Math.floor(56 * multiplier) }
        ],
        zeroQueries: [
            { term: 'custom website design', count: Math.floor(12 * multiplier) }
        ],
        listingPerformance: [
            { center: 'Downtown Hub', brand: 'OutClaw', city: 'Austin', imp: Math.floor(12400 * multiplier), clicks: Math.floor(850 * multiplier), leads: Math.floor(45 * multiplier), rate: '5.2%' }
        ]
    };
}

function renderDashboard(data) {
    // 1. Update Platform Totals
    document.getElementById('val-sessions').innerText = data.totals.sessions.toLocaleString();
    document.getElementById('val-visitors').innerText = data.totals.visitors.toLocaleString();
    document.getElementById('val-leads').innerText = data.totals.leads.toLocaleString();
    document.getElementById('val-searches').innerText = data.totals.searches.toLocaleString();
    document.getElementById('val-impressions').innerText = data.totals.impressions.toLocaleString();
    document.getElementById('val-search-conv').innerText = data.totals.searchConv;

    // Reset trends for now (since we don't have historical delta logic here yet)
    const trends = ['trend-sessions', 'trend-visitors', 'trend-leads', 'trend-searches', 'trend-impressions'];
    trends.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerText = 'Live';
    });

    // 2. Lead Actions Chart (Bar)
    if (leadActionsChart) leadActionsChart.destroy();
    const ctxLead = document.getElementById('leadActionsChart').getContext('2d');
    leadActionsChart = new Chart(ctxLead, {
        type: 'bar',
        data: {
            labels: data.leadActions.labels,
            datasets: [
                {
                    label: 'Website Clicks',
                    data: data.leadActions.website,
                    backgroundColor: '#5AADDB'
                },
                {
                    label: 'Directions',
                    data: data.leadActions.directions,
                    backgroundColor: '#F4678A'
                },
                {
                    label: 'Phone Calls',
                    data: data.leadActions.phone,
                    backgroundColor: '#FF7E5A'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { stacked: true, grid: { display: false } },
                y: { stacked: true, grid: { borderDash: [4, 4] } }
            },
            plugins: {
                legend: { position: 'top', labels: { font: { family: 'DM Sans' } } }
            }
        }
    });

    // 3. Discovery Paths Chart (Pie)
    if (discoveryPathsChart) discoveryPathsChart.destroy();
    const ctxPath = document.getElementById('discoveryPathsChart').getContext('2d');
    const totalPaths = data.discoveryPaths.reduce((sum, item) => sum + item.value, 0);
    
    discoveryPathsChart = new Chart(ctxPath, {
        type: 'pie',
        data: {
            labels: data.discoveryPaths.map(d => `${d.name} (${Math.round((d.value/totalPaths)*100)}%)`),
            datasets: [{
                data: data.discoveryPaths.map(d => d.value),
                backgroundColor: ['#5AADDB', '#B8DFF0', '#F1F5F9'],
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right', labels: { font: { family: 'DM Sans' }, boxWidth: 12 } }
            }
        }
    });

    // 4. Search Intelligence
    document.getElementById('top-queries-list').innerHTML = data.topQueries.map(q => `
        <div class="intel-item">
            <span class="term">${q.term}</span>
            <span class="val">${q.clicks} clicks</span>
        </div>
    `).join('');

    document.getElementById('zero-queries-list').innerHTML = data.zeroQueries.map(q => `
        <div class="intel-item">
            <span class="term">${q.term}</span>
            <span class="val">${q.count} searches</span>
        </div>
    `).join('');

    // 5. Listing Performance
    document.getElementById('listing-performance-body').innerHTML = data.listingPerformance.map(row => `
        <tr>
            <td style="font-weight: 500;">${row.center}</td>
            <td>${row.brand}</td>
            <td>${row.city}</td>
            <td>${row.imp.toLocaleString()}</td>
            <td>${row.clicks.toLocaleString()}</td>
            <td>${row.leads.toLocaleString()}</td>
            <td><span class="rate-badge">${row.rate}</span></td>
        </tr>
    `).join('');
}
