(function() {
  // 1. Determine if this is an article page (inside guides/ but not guide index)
  const path = window.location.pathname;
  const isArticle = path.includes('/guides/') && !path.endsWith('/guides/') && !path.endsWith('/guides/index.html') && !path.endsWith('/guides/');
  
  let slug = 'none';
  let category = 'none';
  
  if (isArticle) {
    slug = path.split('/').pop().replace('.html', '') || 'none';
    const eyebrow = document.querySelector('.eyebrow');
    const firstTag = document.querySelector('.tag-chip');
    category = eyebrow ? eyebrow.textContent.trim() : (firstTag ? firstTag.textContent.trim() : 'Guides');
  }

  // 2. Track Article View on Load
  if (isArticle) {
    window.gtag('event', 'article_view', {
      'article_slug': slug,
      'article_category': category
    });
    console.log('GA4 Tracking: Tracked article_view:', slug, category);
  }

  // 3. Scroll Depth Tracking (50% and 90%)
  let scroll50Fired = false;
  let scroll90Fired = false;
  let scrollTimeout = null;

  function handleScroll() {
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (docHeight <= 0) return;

    const scrollPercent = (window.scrollY / docHeight) * 100;

    if (scrollPercent >= 50 && !scroll50Fired) {
      scroll50Fired = true;
      window.gtag('event', 'scroll_depth', {
        'article_slug': slug,
        'depth_percent': 50
      });
      console.log('GA4 Tracking: Tracked scroll_depth 50%');
    }
    if (scrollPercent >= 90 && !scroll90Fired) {
      scroll90Fired = true;
      window.gtag('event', 'scroll_depth', {
        'article_slug': slug,
        'depth_percent': 90
      });
      console.log('GA4 Tracking: Tracked scroll_depth 90%');
    }
  }

  if (isArticle) {
    window.addEventListener('scroll', function() {
      // Throttle scroll events for performance
      if (scrollTimeout) return;
      scrollTimeout = setTimeout(function() {
        scrollTimeout = null;
        handleScroll();
      }, 250);
    });
  }

  // 4. Global Click Listener for CTA Clicks
  document.addEventListener('click', function(e) {
    const target = e.target.closest('a, button');
    if (!target) return;

    const href = target.getAttribute('href') || '';
    const text = (target.innerText || target.value || '').toLowerCase().trim();
    
    const isNewsletterLink = href.includes('newsletter') || 
                             target.classList.contains('nav-cta') || 
                             target.classList.contains('cta-banner-btn') || 
                             target.id === 'hg-btn' || 
                             text.includes('subscribe');
    
    if (isNewsletterLink) {
      let location = 'inline';
      if (target.closest('nav') || target.closest('.navbar') || target.closest('.nav-drawer')) {
        location = 'nav';
      } else if (target.closest('footer') || target.closest('.site-footer')) {
        location = 'footer';
      } else if (target.closest('.cta-banner')) {
        location = 'inline';
      }
      
      window.gtag('event', 'cta_click', {
        'cta_location': location,
        'article_slug': isArticle ? slug : 'none'
      });
      console.log('GA4 Tracking: Tracked cta_click at location:', location);
    }
  });

  // 5. Form Submission Tracking (Beehiiv Redirect Form)
  document.addEventListener('submit', function(e) {
    const form = e.target;
    if (form.action && form.action.includes('beehiiv')) {
      window.gtag('event', 'newsletter_signup', {
        'method': 'beehiiv_redirect',
        'article_slug': isArticle ? slug : 'none'
      });
      console.log('GA4 Tracking: Tracked newsletter_signup (beehiiv redirect submit)');
    }
  });

  // 6. Intercept Inline Guide CTA Banner Validation Success
  function wrapHandleSubscribe() {
    if (typeof window.handleSubscribe === 'function' && !window.handleSubscribe._wrapped) {
      const original = window.handleSubscribe;
      window.handleSubscribe = function(inputId, btnId) {
        const input = document.getElementById(inputId);
        const email = input ? input.value.trim() : '';
        original(inputId, btnId);
        
        const btn = document.getElementById(btnId);
        // If handleSubscribe succeeded, it disables the button
        if (btn && btn.disabled && email && email.includes('@')) {
          window.gtag('event', 'newsletter_signup', {
            'method': 'cta_banner_form',
            'article_slug': isArticle ? slug : 'none'
          });
          console.log('GA4 Tracking: Tracked newsletter_signup (cta banner success)');
        }
      };
      window.handleSubscribe._wrapped = true;
      console.log('GA4 Tracking: Successfully wrapped window.handleSubscribe');
    }
  }

  // Attempt wrapping at script load time, DOM ready, and fully loaded
  wrapHandleSubscribe();
  document.addEventListener('DOMContentLoaded', wrapHandleSubscribe);
  window.addEventListener('load', wrapHandleSubscribe);
})();
