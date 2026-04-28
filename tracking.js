(function() {
  const SB_URL = 'https://pjxoyoomnaglrzwdvelv.supabase.co';
  const SB_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBqeG95b29tbmFnbHJ6d2R2ZWx2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczMjEyMDgsImV4cCI6MjA5Mjg5NzIwOH0.75QblYTeXI7WAkiUSEFCwB3F0B2WCHs9QJe0v5PX4NY';
  
  // Wait for Supabase to be loaded if script is external
  function init() {
    if (!window.supabase) {
      setTimeout(init, 100);
      return;
    }
    
    const supabase = window.supabase.createClient(SB_URL, SB_KEY);
    console.log('Supabase tracking initialized');

    async function trackEvent(type, data = {}, source = null) {
      console.log('Tracking event:', type, data);
      try {
        const { error } = await supabase.from('analytics_events').insert([{
          event_type: type,
          event_data: data,
          source: source || (document.referrer.includes('google') ? 'search' : (document.referrer ? 'browse' : 'direct')),
          created_at: new Date().toISOString()
        }]);
        if (error) console.error('Supabase insert error:', error);
        else console.log('Event tracked successfully');
      } catch (e) { console.error('Tracking exception:', e); }
    }

    // Initial visit
    trackEvent('session_start');

    // Track search query from URL
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');
    if (query) {
      trackEvent('search', { query: query, results: 1 }); // Assume 1 result for now
    }

    // Global Click Listener
    document.addEventListener('click', function(e) {
      const target = e.target.closest('a, button');
      if (!target) return;

      const text = (target.innerText || target.value || '').toLowerCase().trim();
      
      // Lead Actions
      if (text.includes('subscribe') || text.includes('get started') || text.includes('join') || text.includes('download')) {
        trackEvent('lead_action', { type: 'website', label: text });
      }
      
      // Outbound clicks
      if (target.tagName === 'A' && target.href.includes('http') && !target.href.includes(window.location.hostname)) {
        trackEvent('click', { url: target.href, label: text });
      }
    });
  }

  init();
})();
