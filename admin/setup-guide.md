# Admin Dashboard Setup Guide

This dashboard tracks KPIs for `outclaw.xyz`. You can fetch data using two methods: **Session-Based (Manual Sync)** or **Serverless (Automated)**.

## Method A: Session-Based (Easiest)
This uses your browser's current Google login to "Sync" data directly to the dashboard.
1.  **Google Cloud Console**: Create an **OAuth 2.0 Client ID** (Web application).
2.  **Authorized Origins**: Add `https://outclaw.xyz` (and `http://localhost` for testing).
3.  **Update `admin/dashboard.js`**: Paste your `CLIENT_ID` into the constant at the top.
4.  **Usage**: In the dashboard, click **"Connect Google Session"**. This will prompt you to sign in and grant read-only access.

## Method B: Serverless (Live Updates)
To fetch data automatically in the background without needing to sign in every time:
1.  **Google Cloud Console**: Enable **Google Analytics Data API** and **Search Console API**.
2.  **Service Account**: Create a Service Account, download the JSON key, and add the Service Account email as a "Viewer" in your GA4 Property settings.
3.  **Environment Variables**: Add your `GA_PROPERTY_ID` and `GOOGLE_APPLICATION_CREDENTIALS` to your Netlify/Hosting provider.

## 2. Google Search Console (GSC)
To fetch "Search Clicks" and "Impressions":
1.  **Google Cloud Console**: Enable the **Google Search Console API**.
2.  **Permissions**: Ensure the same Service Account has "Viewer" access to your site in GSC.
3.  **Endpoint**: Use the `searchAnalytics.query` method to fetch data for the last 30 days.

## 3. Beehiiv (Newsletter)
To fetch "Total Subscribers":
1.  **Beehiiv Dashboard**: Go to Settings → API and generate an API Key.
2.  **Publication ID**: Your ID is already configured in the dashboard (`pub_d2d894cb-7763-4399-8a6e-096904a48845`).

## 4. Making it "Live"
Since this is a static site, you should use a **Serverless Function** (e.g., Netlify Functions) to proxy these requests securely without exposing your API keys.

### Example Node.js Function (`netlify/functions/get-metrics.js`)
```javascript
const { BetaAnalyticsDataClient } = require('@google-analytics/data');

exports.handler = async () => {
  const analyticsClient = new BetaAnalyticsDataClient();
  // Fetch GA4 Data...
  // Fetch GSC Data...
  // Fetch Beehiiv Data...
  
  return {
    statusCode: 200,
    body: JSON.stringify({
      users: ga4_data,
      clicks: gsc_data,
      subs: beehiiv_data
    })
  };
};
```

## 5. Dashboard Authentication
The current access key is: `outclaw2026`.
You can change this in `admin/dashboard.js`. For production, it is recommended to use **Netlify Identity** or **Firebase Auth** for robust security.
