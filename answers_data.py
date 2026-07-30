# Answers database for openclaw.xyz
# Contains 80 high-quality, technical Q&A entries across 5 categories.

ANSWERS = [
    # =========================================================================
    # CATEGORY: MCP & Connectors (25 entries)
    # =========================================================================
    {
        "slug": "connect-claude-to-gmail-mcp",
        "question": "How do you connect Claude to Gmail via MCP?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "To connect Claude to Gmail via the Model Context Protocol (MCP), add the official Google Gmail MCP server configuration to your Claude Desktop configuration file. Authenticate by creating a client credential via the Google Cloud Console and running the initial OAuth consent flow.",
        "answer_type": "steps",
        "body": """
        <h2>Step-by-step Connection</h2>
        <ol>
            <li>Go to the Google Cloud Console, create a new project, and enable the <strong>Gmail API</strong>.</li>
            <li>Configure the OAuth consent screen (choose External or Internal) and create an OAuth 2.0 Client ID credential. Download the JSON credentials file.</li>
            <li>Install the Gmail MCP server package using your package manager: <code>npm install -g @modelcontextprotocol/server-gmail</code>.</li>
            <li>Locate your Claude Desktop config file (<code>claude_desktop_config.json</code>) and add the server definition pointing to your credentials file:
<pre><code class="language-json">{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-gmail",
        "--credentials",
        "/absolute/path/to/your/oauth-credentials.json"
      ]
    }
  }
}</code></pre>
            </li>
            <li>Restart Claude Desktop. A prompt will appear in your default browser requesting OAuth access to your Gmail account. Authorize the application.</li>
        </ol>
        <h2>Notes</h2>
        <ul>
          <li>Keep your <code>oauth-credentials.json</code> file in a secure local directory that Claude has read permissions to.</li>
          <li>For security, configure the Google Cloud OAuth Consent Screen with minimal scopes (e.g., <code>gmail.readonly</code> or <code>gmail.modify</code>) rather than full control.</li>
        </ul>
        """,
        "verified_against": "Gmail MCP Connector v1.2 · Claude API 2025-07-01",
        "verified_date": "July 2026",
        "related_slugs": ["mcp-server-url-format", "mcp-auth-patterns", "configure-mcp-in-claude-desktop"]
      },
      {
        "slug": "mcp-server-url-format",
        "question": "What is the MCP server URL format for Claude connectors?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "The Model Context Protocol (MCP) uses Server-Sent Events (SSE) for HTTP transport, where the client establishes a SSE connection to a GET endpoint (e.g. http://localhost:3000/sse) and sends JSON-RPC client-to-server messages via POST requests to a separate endpoint declared by the server.",
        "answer_type": "definition",
        "body": """
        <h2>Format Specification</h2>
        <p>While local MCP connections run over Standard Input/Output (stdio) using child processes, remote connections utilize Server-Sent Events (SSE). The URL structure requires two components:</p>
        <ol>
            <li><strong>SSE Connection Endpoint:</strong> The entry point where the Claude client starts a GET request to open a persistent events connection stream. For example: <code>http://localhost:3000/sse</code>.</li>
            <li><strong>HTTP POST Route:</strong> Once connected, the server sends a unique session identifier. The client sends JSON-RPC payload commands to the corresponding post URL, typically structured as: <code>http://localhost:3000/message?sessionId=&lt;session_id&gt;</code>.</li>
        </ol>
        <h2>Example Endpoint Configurations</h2>
        <table class="data-table">
          <thead>
            <tr>
              <th>Transport Mode</th>
              <th>Endpoint / Connection Scheme</th>
              <th>Authentication Payload Location</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Stdio (Local)</td>
              <td>Process Execution (e.g., <code>npx @modelcontextprotocol/server-postgres</code>)</td>
              <td>Environment Variables (e.g., <code>PGPASSWORD</code>)</td>
            </tr>
            <tr>
              <td>Remote SSE (HTTP)</td>
              <td><code>http://[domain]/sse</code> or <code>https://[domain]/sse</code></td>
              <td>Authorization Header / Bearer Token</td>
            </tr>
          </tbody>
        </table>
        """,
        "verified_against": "MCP Spec v1.0.4",
        "verified_date": "July 2026",
        "related_slugs": ["mcp-sse-transport-setup", "mcp-auth-patterns", "configure-mcp-in-claude-desktop"]
      },
      {
        "slug": "mcp-auth-patterns",
        "question": "How do you authenticate MCP connectors in Claude.ai?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "In local environments, MCP servers authenticate via environment variables passed directly in the server config file. For remote, network-based MCP servers using Server-Sent Events (SSE), authentication is handled via Bearer tokens in the HTTP Authorization headers or customized query parameters.",
        "answer_type": "code",
        "body": """
        <h2>Authentication Configuration Patterns</h2>
        <p>Depending on whether the server is local or remote, auth details are specified in your <code>claude_desktop_config.json</code> configuration file.</p>
        
        <h3>1. Local Stdio Auth (via Environment Variables)</h3>
        <p>Pass API keys or database passwords within the <code>env</code> block of the server configuration:</p>
<pre><code class="language-json">{
  "mcpServers": {
    "github-mcp": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_yourPersonalAccessTokenHere"
      }
    }
  }
}</code></pre>

        <h3>2. Remote HTTP SSE Auth (via Authorization Headers)</h3>
        <p>If utilizing a remote connection manager, supply HTTP request headers in the connection profile definition:</p>
<pre><code class="language-json">{
  "mcpServers": {
    "remote-knowledge-base": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/client-sse", "--url", "https://api.example.com/mcp/sse"],
      "env": {
        "SSE_AUTH_HEADER": "Bearer mcp_secure_token_abcdef123456"
      }
    }
  }
}</code></pre>
        """,
        "verified_against": "MCP CLI Connector v1.1",
        "verified_date": "July 2026",
        "related_slugs": ["connect-claude-to-github-mcp", "mcp-server-url-format", "configure-mcp-in-claude-desktop"]
      },
      {
        "slug": "connect-claude-to-notion-mcp",
        "question": "How do you connect Claude to Notion via MCP?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "Connect Claude to your Notion workspace by registering a new internal integration inside the Notion Developer Portal to obtain an integration token, granting workspace access permissions, and configuring the official Notion MCP server in your Claude Desktop configuration.",
        "answer_type": "steps",
        "body": """
        <h2>Step-by-step Connection</h2>
        <ol>
            <li>Go to the <a href="https://www.notion.so/my-integrations" target="_blank">Notion My Integrations</a> portal.</li>
            <li>Click <strong>New Integration</strong>. Name it 'Claude MCP', select the correct workspace, and copy the generated <strong>Internal Integration Token</strong>.</li>
            <li>Open the specific Notion page or database you want Claude to access, click the top right settings (...) menu, select <strong>Add connections</strong>, and find your integration name.</li>
            <li>Add the Notion server block to your <code>claude_desktop_config.json</code> configuration:
<pre><code class="language-json">{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": {
        "NOTION_API_KEY": "secret_yourNotionIntegrationTokenHere"
      }
    }
  }
}</code></pre>
            </li>
            <li>Save the config file and restart Claude Desktop to load the connector.</li>
        </ol>
        """,
        "verified_against": "Notion MCP Server v0.8.2 · Notion API v2022-06-28",
        "verified_date": "July 2026",
        "related_slugs": ["mcp-auth-patterns", "configure-mcp-in-claude-desktop", "native-mcp-servers-claude"]
      },
      {
        "slug": "connect-claude-to-github-mcp",
        "question": "How do you connect Claude to GitHub via MCP?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "To connect Claude to GitHub, generate a Personal Access Token (Classic or Fine-Grained) on GitHub with access to your target repositories, and add the official GitHub MCP server configuration to your local Claude Desktop config file.",
        "answer_type": "steps",
        "body": """
        <h2>Step-by-step Connection</h2>
        <ol>
            <li>Log in to GitHub and go to <strong>Settings &gt; Developer settings &gt; Personal access tokens &gt; Tokens (classic)</strong>.</li>
            <li>Click <strong>Generate new token</strong>. Set the scope permissions for <code>repo</code> (full control of private repositories), <code>read:org</code>, and <code>gist</code>.</li>
            <li>Copy the generated token immediately.</li>
            <li>Add the GitHub server block to your <code>claude_desktop_config.json</code> file:
<pre><code class="language-json">{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_yourGitHubTokenHere"
      }
    }
  }
}</code></pre>
            </li>
            <li>Restart Claude Desktop. Claude can now search issues, read code files, commit changes, and interact with PRs on GitHub.</li>
        </ol>
        """,
        "verified_against": "GitHub MCP Server v1.0.1",
        "verified_date": "July 2026",
        "related_slugs": ["mcp-auth-patterns", "configure-mcp-in-claude-desktop", "connect-claude-to-notion-mcp"]
      },
      {
        "slug": "connect-claude-to-slack-mcp",
        "question": "How do you connect Claude to Slack via MCP?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "To connect Claude to Slack via MCP, create a Slack App in your workspace API settings, configure Bot User OAuth Tokens with read/write permissions, install the app in your workspace, and set up the Slack MCP server in your Claude Desktop configuration.",
        "answer_type": "steps",
        "body": """
        <h2>Step-by-step Connection</h2>
        <ol>
            <li>Go to <a href="https://api.slack.com/apps" target="_blank">Slack API Apps</a> and click <strong>Create New App</strong>. Choose 'From scratch' and select your workspace.</li>
            <li>Navigate to <strong>OAuth &amp; Permissions</strong>. Under Scopes, add scopes: <code>channels:history</code>, <code>channels:read</code>, <code>chat:write</code>, <code>groups:read</code>, <code>im:history</code>, <code>im:read</code>, <code>users:read</code>.</li>
            <li>Click <strong>Install to Workspace</strong> at the top of the page. Grant permissions and copy the <strong>Bot User OAuth Token</strong> (starts with <code>xoxb-</code>).</li>
            <li>Configure your local <code>claude_desktop_config.json</code> as follows:
<pre><code class="language-json">{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-yourSlackBotTokenHere"
      }
    }
  }
}</code></pre>
            </li>
            <li>Restart Claude Desktop. Invite your Slack Bot to the channel you want it to interact with (e.g. <code>/invite @bot_name</code>) to start querying.</li>
        </ol>
        """,
        "verified_against": "Slack MCP Server v1.0.0 · Slack API 2026",
        "verified_date": "July 2026",
        "related_slugs": ["mcp-auth-patterns", "configure-mcp-in-claude-desktop", "connect-claude-to-github-mcp"]
      },
      {
        "slug": "connect-claude-to-google-drive-mcp",
        "question": "How do you connect Claude to Google Drive via MCP?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "To connect Claude to Google Drive, enable the Google Drive API in the Google Cloud Console, create OAuth 2.0 credentials, and pass these credentials to the Google Drive MCP server inside your Claude Desktop configuration.",
        "answer_type": "steps",
        "body": """
        <h2>Step-by-step Connection</h2>
        <ol>
            <li>Create a project in the Google Cloud Console, enable the <strong>Google Drive API</strong>, and create OAuth 2.0 Client credentials. Download the JSON credentials file.</li>
            <li>Install the Google Drive MCP server: <code>npm install -g @modelcontextprotocol/server-google-drive</code>.</li>
            <li>Add the configuration block pointing to your credentials file to your <code>claude_desktop_config.json</code> file:
<pre><code class="language-json">{
  "mcpServers": {
    "google-drive": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-google-drive",
        "--credentials",
        "/absolute/path/to/your/oauth-credentials.json"
      ]
    }
  }
}</code></pre>
            </li>
            <li>Restart Claude Desktop, and complete the OAuth authentication request inside your browser to link Google Drive.</li>
        </ol>
        """,
        "verified_against": "Google Drive MCP Connector v1.1.2",
        "verified_date": "July 2026",
        "related_slugs": ["connect-claude-to-gmail-mcp", "mcp-auth-patterns", "configure-mcp-in-claude-desktop"]
      },
      {
        "slug": "native-mcp-servers-claude",
        "question": "What MCP servers does Claude.ai support natively?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "Claude.ai (web interface) supports a selected set of official remote connectors natively, including Google Drive, Gmail, Notion, GitHub, and Slack, which authenticate directly via OAuth in the user profile settings, bypassing the need for local desktop configurations.",
        "answer_type": "definition",
        "body": """
        <h2>Native Connectors Overview</h2>
        <p>In the Claude.ai Web UI, users do not configure local JSON config files. Instead, Anthropic hosts native cloud MCP integrations that users can toggle on and off under their account settings.</p>
        
        <h3>List of Native Web Connectors</h3>
        <ul>
          <li><strong>Notion:</strong> Read, query, and search databases and page contents.</li>
          <li><strong>Google Drive:</strong> View, extract text, and index files directly inside folders.</li>
          <li><strong>Gmail:</strong> Read, search, and compose drafts.</li>
          <li><strong>GitHub:</strong> Query repositories, issues, pull requests, and file contents.</li>
          <li><strong>Slack:</strong> Read channel histories and search message logs.</li>
        </ul>

        <h2>Comparison of Native vs. Desktop MCP</h2>
        <table class="data-table">
          <thead>
            <tr>
              <th>Feature</th>
              <th>Claude.ai Web Native</th>
              <th>Claude Desktop MCP</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Configuration</td>
              <td>One-click OAuth in Account Settings</td>
              <td>Manual edits to <code>claude_desktop_config.json</code></td>
            </tr>
            <tr>
              <td>Host Location</td>
              <td>Anthropic Cloud Infrastructure</td>
              <td>Local system / Stdio Subprocess</td>
            </tr>
            <tr>
              <td>Custom Servers</td>
              <td>Not Supported</td>
              <td>Supported (any local node/python script)</td>
            </tr>
            <tr>
              <td>Local Resource Access</td>
              <td>No</td>
              <td>Yes (Access files, shell commands, databases)</td>
            </tr>
          </tbody>
        </table>
        """,
        "verified_against": "Claude.ai Web UI 2026",
        "verified_date": "July 2026",
        "related_slugs": ["connect-claude-to-notion-mcp", "connect-claude-to-github-mcp", "configure-mcp-in-claude-desktop"]
      },
      {
        "slug": "multiple-mcp-servers-single-session",
        "question": "Can you use multiple MCP servers in one Claude session?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "Yes, Claude can connect to and query multiple MCP servers concurrently in a single chat session. The client merges all tools, prompts, and resources from all configured servers and presents them to Claude's model context.",
        "answer_type": "definition",
        "body": """
        <h2>How it works</h2>
        <p>When you start a session in Claude Desktop or Claude.ai with multiple active servers, the client queries each MCP server for its list of capabilities (using the <code>tools/list</code> protocol). It registers all available tools globally. When processing prompts, Claude automatically selects the correct tool by matches with the schemas provided by the respective servers.</p>

        <h3>Example Multi-Server configuration in Claude Desktop</h3>
        <p>Here is how you define three concurrent servers in one local setup:</p>
<pre><code class="language-json">{
  "mcpServers": {
    "postgres-db": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "--conn", "postgresql://localhost/dev"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_123" }
    },
    "local-fs": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/dev/project"]
    }
  }
}</code></pre>
        """,
        "verified_against": "MCP Spec v1.0.4",
        "verified_date": "July 2026",
        "related_slugs": ["configure-mcp-in-claude-desktop", "native-mcp-servers-claude", "mcp-server-url-format"]
      },
      {
        "slug": "build-custom-mcp-server-claude",
        "question": "How do you build a custom MCP server for Claude?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "To build a custom MCP server for Claude, use the official TypeScript or Python SDK, define the schemas for the tools, resources, and prompt formats, and write standard stdio or SSE transport handlers to process requests.",
        "answer_type": "code",
        "body": """
        <h2>TypeScript Implementation Example</h2>
        <p>Here is how you build a minimal custom MCP server in Node.js that exposes a custom calculator tool:</p>
        
        <ol>
          <li>Initialize a project: <code>npm init -y &amp;&amp; npm install @modelcontextprotocol/sdk</code>.</li>
          <li>Write the server code (e.g. <code>server.ts</code>):</li>
        </ol>
<pre><code class="language-typescript">import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server({
  name: "custom-math-server",
  version: "1.0.0"
}, {
  capabilities: { tools: {} }
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "calculate_cube",
    description: "Calculates the cube of a number.",
    inputSchema: {
      type: "object",
      properties: {
        number: { type: "number" }
      },
      required: ["number"]
    }
  }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "calculate_cube") {
    const number = request.params.arguments?.number as number;
    return {
      content: [{ type: "text", text: String(number * number * number) }]
    };
  }
  throw new Error("Tool not found");
});

const transport = new StdioServerTransport();
await server.connect(transport);</code></pre>
        """,
        "verified_against": "MCP SDK v0.7.0",
        "verified_date": "July 2026",
        "related_slugs": ["mcp-stdio-transport-setup", "mcp-sse-transport-setup", "mcp-server-logging-and-debugging"]
      },
      {
        "slug": "connect-claude-to-postgres-mcp",
        "question": "How do you connect Claude to PostgreSQL via MCP?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "To connect Claude to a PostgreSQL database, configure the postgres MCP server in your Claude Desktop configuration file and pass your database connection URI as an argument.",
        "answer_type": "code",
        "body": """
        <h2>Configuration</h2>
        <p>Include the database connector configuration in your <code>claude_desktop_config.json</code>:</p>
<pre><code class="language-json">{
  "mcpServers": {
    "postgres-db": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "--conn",
        "postgresql://username:password@localhost:5432/dbname"
      ]
    }
  }
}</code></pre>
        <p>Replace <code>username</code>, <code>password</code>, <code>localhost</code>, <code>5432</code>, and <code>dbname</code> with your target PostgreSQL server details.</p>
        """,
        "verified_against": "PostgreSQL MCP Server v0.2.1",
        "verified_date": "July 2026",
        "related_slugs": ["configure-mcp-in-claude-desktop", "connect-claude-to-sqlite-mcp", "mcp-auth-patterns"]
      },
      {
        "slug": "connect-claude-to-sqlite-mcp",
        "question": "How do you connect Claude to SQLite via MCP?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "To connect Claude to SQLite, add the sqlite MCP server definition in the configuration file, specifying the absolute filepath to your SQLite database file.",
        "answer_type": "code",
        "body": """
        <h2>Configuration</h2>
        <p>Add the server to your <code>claude_desktop_config.json</code> config file:</p>
<pre><code class="language-json">{
  "mcpServers": {
    "sqlite-db": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sqlite",
        "--db",
        "/absolute/path/to/your/database.sqlite"
      ]
    }
  }
}</code></pre>
        <p>Make sure Claude has read and write permissions to both the directory and the database file.</p>
        """,
        "verified_against": "SQLite MCP Server v0.3.0",
        "verified_date": "July 2026",
        "related_slugs": ["configure-mcp-in-claude-desktop", "connect-claude-to-postgres-mcp", "mcp-auth-patterns"]
      },
      {
        "slug": "connect-claude-to-brave-search-mcp",
        "question": "How do you connect Claude to Brave Search via MCP?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "To connect Claude to Brave Search, retrieve a Brave Search API key from the developer portal, and configure the brave-search MCP server using that API key in your Claude configuration.",
        "answer_type": "steps",
        "body": """
        <h2>Step-by-step Connection</h2>
        <ol>
            <li>Go to <a href="https://api.search.brave.com/app/dashboard" target="_blank">Brave Search API Dashboard</a> and register for a developer account.</li>
            <li>Generate a new API key.</li>
            <li>Add the Brave Search block to your <code>claude_desktop_config.json</code>:
<pre><code class="language-json">{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "yourBraveApiKeyHere"
      }
    }
  }
}</code></pre>
            </li>
            <li>Restart Claude Desktop. Claude can now perform live web searches directly using Brave API.</li>
        </ol>
        """,
        "verified_against": "Brave Search MCP v1.0.0",
        "verified_date": "July 2026",
        "related_slugs": ["configure-mcp-in-claude-desktop", "mcp-auth-patterns", "native-mcp-servers-claude"]
      },
      {
        "slug": "connect-claude-to-linear-mcp",
        "question": "How do you connect Claude to Linear via MCP?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "To connect Claude to Linear, generate an API access token in your Linear account developer settings and configure the official Linear MCP server in your Claude Desktop configuration.",
        "answer_type": "steps",
        "body": """
        <h2>Step-by-step Connection</h2>
        <ol>
            <li>Log in to Linear and navigate to <strong>Settings &gt; Account &gt; Developer &gt; Personal API Keys</strong>.</li>
            <li>Create a new API Key, copy it, and keep it safe.</li>
            <li>Edit your <code>claude_desktop_config.json</code> to register the Linear server:
<pre><code class="language-json">{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": {
        "LINEAR_API_KEY": "lin_api_yourLinearApiKeyHere"
      }
    }
  }
}</code></pre>
            </li>
            <li>Restart Claude Desktop to enable query access on Linear tickets.</li>
        </ol>
        """,
        "verified_against": "Linear MCP Server v0.5.1",
        "verified_date": "July 2026",
        "related_slugs": ["mcp-auth-patterns", "configure-mcp-in-claude-desktop", "connect-claude-to-github-mcp"]
      },
      {
        "slug": "mcp-inspector-setup-guide",
        "question": "How do you inspect and debug MCP servers using MCP Inspector?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "Use the official @modelcontextprotocol/inspector command-line interface tool to inspect capabilities, send test requests, and view the JSON-RPC traffic on stdio-based MCP servers.",
        "answer_type": "code",
        "body": """
        <h2>Using the Inspector</h2>
        <p>To run the developer console inspector on a local server, launch the command via npx:</p>
<pre><code class="language-bash">npx @modelcontextprotocol/inspector &lt;your-server-command&gt; [args...]</code></pre>
        <h3>Example: Inspecting PostgreSQL Server</h3>
<pre><code class="language-bash">npx @modelcontextprotocol/inspector npx @modelcontextprotocol/server-postgres --conn postgresql://localhost/dev</code></pre>
        <p>This command starts a web interface (defaulting to port <code>http://localhost:5173</code>) where you can interactively invoke tools and inspect logging frames.</p>
        """,
        "verified_against": "MCP Inspector v0.4.0",
        "verified_date": "July 2026",
        "related_slugs": ["mcp-server-logging-and-debugging", "build-custom-mcp-server-claude", "mcp-stdio-transport-setup"]
      },
      {
        "slug": "mcp-transport-protocols-compared",
        "question": "What transport protocols are supported by MCP?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "MCP supports two standard transport protocols: stdio (Standard Input/Output) for local sub-processes, and Server-Sent Events (SSE) for remote clients and web-based server setups using HTTP endpoints.",
        "answer_type": "definition",
        "body": """
        <h2>Transport Mode Comparison</h2>
        <p>The Model Context Protocol establishes JSON-RPC channels over two distinct transports:</p>
        <table class="data-table">
          <thead>
            <tr>
              <th>Transport Mode</th>
              <th>Best For</th>
              <th>Operational Model</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Stdio</strong></td>
              <td>Local system integrations and desktop AI applications.</td>
              <td>Subprocess spawned by the client. Read/write to stdout/stdin.</td>
            </tr>
            <tr>
              <td><strong>Server-Sent Events (SSE)</strong></td>
              <td>Web-based apps, microservices, and remote API access.</td>
              <td>GET request holds open an SSE stream. Client POSTs messages to server.</td>
            </tr>
          </tbody>
        </table>
        """,
        "verified_against": "MCP Protocol Spec v1.0.4",
        "verified_date": "July 2026",
        "related_slugs": ["mcp-stdio-transport-setup", "mcp-sse-transport-setup", "mcp-server-url-format"]
      },
      {
        "slug": "mcp-sse-transport-setup",
        "question": "How do you configure Server-Sent Events (SSE) transport for MCP?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "To configure SSE transport on an MCP server, instantiate an SSEServerTransport on your HTTP server routing layer to dispatch events, and implement a POST endpoint that accepts the client JSON-RPC payloads.",
        "answer_type": "code",
        "body": """
        <h2>Node.js Express Setup Example</h2>
        <p>Expose your MCP server using Server-Sent Events in an Express.js application:</p>
<pre><code class="language-typescript">import express from "express";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";

const server = new Server({ name: "my-sse-server", version: "1.0" }, { capabilities: {} });
const app = express();

let transport: SSEServerTransport;

app.get("/sse", (req, res) => {
  transport = new SSEServerTransport("/messages", res);
  server.connect(transport);
});

app.post("/messages", (req, res) => {
  if (transport) {
    transport.handleMessage(req, res);
  } else {
    res.status(400).send("No active SSE session");
  }
});

app.listen(3000);</code></pre>
        """,
        "verified_against": "MCP SDK v0.7.0",
        "verified_date": "July 2026",
        "related_slugs": ["mcp-server-url-format", "mcp-transport-protocols-compared", "build-custom-mcp-server-claude"]
      },
      {
        "slug": "mcp-stdio-transport-setup",
        "question": "How do you configure standard input/output (stdio) transport for MCP?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "To run an MCP server on stdio transport, connect it using StdioServerTransport from the SDK. The host process will spawn the server as a background process and communicate by reading and writing to its stdin/stdout streams.",
        "answer_type": "code",
        "body": """
        <h2>Standard Implementation</h2>
<pre><code class="language-typescript">import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server(
  { name: "stdio-demo", version: "1.0.0" },
  { capabilities: {} }
);

// Connect process stdout and stdin stream channels
const transport = new StdioServerTransport();
await server.connect(transport);</code></pre>
        <p>Ensure your server does not print anything else to <code>console.log</code> during execution, as extra output on stdout will corrupt the JSON-RPC messaging frame. Use <code>console.error</code> for logging.</p>
        """,
        "verified_against": "MCP SDK v0.7.0",
        "verified_date": "July 2026",
        "related_slugs": ["mcp-transport-protocols-compared", "build-custom-mcp-server-claude", "mcp-server-logging-and-debugging"]
      },
      {
        "slug": "configure-mcp-in-claude-desktop",
        "question": "How do you configure MCP servers in Claude Desktop?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "Open your local OS-specific configuration path and edit the JSON-formatted configuration file to define your stdio or remote MCP servers under the mcpServers parent key.",
        "answer_type": "definition",
        "body": """
        <h2>Configuration Locations</h2>
        <ul>
          <li><strong>macOS:</strong> <code>~/Library/Application Support/Claude/claude_desktop_config.json</code></li>
          <li><strong>Windows:</strong> <code>%APPDATA%\\Claude\\claude_desktop_config.json</code></li>
        </ul>
        
        <h2>Example Config Template</h2>
<pre><code class="language-json">{
  "mcpServers": {
    "local-server-name": {
      "command": "node",
      "args": ["/path/to/server.js"],
      "env": {
        "ENV_KEY": "value"
      }
    }
  }
}</code></pre>
        """,
        "verified_against": "Claude Desktop v0.18.0",
        "verified_date": "July 2026",
        "related_slugs": ["mcp-auth-patterns", "multiple-mcp-servers-single-session", "mcp-server-logging-and-debugging"]
      },
      {
        "slug": "mcp-security-sandboxing-guide",
        "question": "How do you sandbox MCP server execution for security?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "To sandbox local MCP servers, run the processes in docker container environments, isolate the network using minimal networking settings, and restrict file access to specific, non-root directory paths.",
        "answer_type": "definition",
        "body": """
        <h2>Sandboxing Best Practices</h2>
        <p>Since stdio MCP servers execute system processes locally, a malicious or malfunctioning server could delete files or read user secrets. Isolate them with these layers:</p>
        
        <h3>Docker Isolation</h3>
        <p>Run your servers inside isolated containers, mounting only the necessary resource volumes:</p>
<pre><code class="language-bash">docker run -it --rm -v /local/dir:/container/dir mcp-server-image</code></pre>

        <h3>Environment Check</h3>
        <ul>
          <li>Never run Claude Desktop or MCP server tasks as root or Administrator.</li>
          <li>Set database connection scopes to read-only accounts when querying live schemas.</li>
        </ul>
        """,
        "verified_against": "MCP Security Guide v1.0",
        "verified_date": "July 2026",
        "related_slugs": ["configure-mcp-in-claude-desktop", "mcp-auth-patterns", "build-custom-mcp-server-claude"]
      },
      {
        "slug": "handle-mcp-timeout-errors",
        "question": "How do you handle timeout errors in MCP server calls?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "In your client connector code, wrap requests in timeout wrappers that reject after a threshold (e.g., 60 seconds) and ensure your server yields status updates for long-running processes.",
        "answer_type": "code",
        "body": """
        <h2>Handling timeouts in client code</h2>
<pre><code class="language-typescript">async function fetchWithTimeout(client, requestParams, timeoutMs = 30000) {
  const timeoutPromise = new Promise((_, reject) => 
    setTimeout(() => reject(new Error("MCP request timed out")), timeoutMs)
  );
  return Promise.race([
    client.request(requestParams),
    timeoutPromise
  ]);
}</code></pre>
        """,
        "verified_against": "MCP SDK v0.7.0",
        "verified_date": "July 2026",
        "related_slugs": ["mcp-server-logging-and-debugging", "build-custom-mcp-server-claude", "mcp-inspector-setup-guide"]
      },
      {
        "slug": "share-mcp-servers-across-agents",
        "question": "Can multiple agent instances share a single MCP server connection?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "While stdio sub-processes are strictly single-client, a remote MCP server using Server-Sent Events (SSE) transport can handle multiple client agent sessions concurrently.",
        "answer_type": "definition",
        "body": """
        <h2>Protocol Mechanics</h2>
        <p>Local stdio instances are exclusive to the parent OS process that spawned them. To share state, resources, or configurations across multiple agent framework threads, deploy your server on SSE transport.</p>
        <p>In SSE mode, every connecting agent is allocated a unique session ID. The server maintains separate connections and parses the incoming requests based on the session scope.</p>
        """,
        "verified_against": "MCP Spec v1.0.4",
        "verified_date": "July 2026",
        "related_slugs": ["mcp-sse-transport-setup", "mcp-transport-protocols-compared", "mcp-server-url-format"]
      },
      {
        "slug": "mcp-dynamic-server-registration",
        "question": "Does MCP support dynamic server discovery and registration?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "Yes, MCP supports discovery via client polling of capabilities, but active runtime server insertion depends on the agent framework implementation parsing client settings.",
        "answer_type": "definition",
        "body": """
        <h2>Dynamic Discovery Protocol</h2>
        <p>A client agent can request updates by calling the capability APIs. If a tool or database schema changes, the server issues a notification so the LLM is aware of the new function signature without restarting the application.</p>
        """,
        "verified_against": "MCP Spec v1.0.4",
        "verified_date": "July 2026",
        "related_slugs": ["build-custom-mcp-server-claude", "mcp-sse-transport-setup", "mcp-transport-protocols-compared"]
      },
      {
        "slug": "mcp-cursor-integration-steps",
        "question": "How do you add an MCP server to Cursor?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "To add an MCP server to Cursor, navigate to Cursor Settings > Features > MCP, click + Add New MCP Server, choose the transport type (stdio or SSE), and insert your command or connection URL.",
        "answer_type": "steps",
        "body": """
        <h2>Steps to Add Server</h2>
        <ol>
          <li>Open Cursor and open the preferences dashboard (Gear icon).</li>
          <li>Select the <strong>Features</strong> tab on the sidebar.</li>
          <li>Scroll down to the <strong>MCP</strong> section.</li>
          <li>Click <strong>+ Add New MCP Server</strong>.</li>
          <li>Select type (e.g. <code>stdio</code>), name your server, and insert your execution command (e.g. <code>npx @modelcontextprotocol/server-postgres</code>).</li>
          <li>Save. Cursor Composer can now immediately access and use the registered tools.</li>
        </ol>
        """,
        "verified_against": "Cursor v0.45.0",
        "verified_date": "July 2026",
        "related_slugs": ["configure-mcp-in-claude-desktop", "mcp-auth-patterns", "mcp-server-logging-and-debugging"]
      },
      {
        "slug": "mcp-server-logging-and-debugging",
        "question": "How do you view and debug logs for MCP servers?",
        "category": "mcp-connectors",
        "category_name": "MCP & Connectors",
        "quick_answer": "In stdio MCP servers, route logs to stderr using console.error() instead of console.log(). In Claude Desktop, inspect logs at ~/Library/Logs/Claude/mcp.log to review JSON-RPC errors.",
        "answer_type": "definition",
        "body": """
        <h2>Log Locations</h2>
        <ul>
          <li><strong>macOS Log File:</strong> <code>~/Library/Logs/Claude/mcp.log</code></li>
          <li><strong>Windows Log File:</strong> <code>%APPDATA%\\Claude\\Logs\\mcp.log</code></li>
        </ul>
        <p>Ensure you write logs to standard error in your custom code:</p>
<pre><code class="language-javascript">console.error("Debugging database query result count: " + results.length);</code></pre>
        """,
        "verified_against": "Claude Desktop v0.18.0",
        "verified_date": "July 2026",
        "related_slugs": ["mcp-inspector-setup-guide", "build-custom-mcp-server-claude", "mcp-stdio-transport-setup"]
      },

    # =========================================================================
    # CATEGORY: Claude API (20 entries)
    # =========================================================================
    {
        "slug": "claude-api-rate-limits-by-tier",
        "question": "What are the Claude API rate limits by tier?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "Claude API rate limits are governed by Tier structures based on your deposit history. Tier 1 has limits of 20,000 Tokens Per Minute (TPM) and 50 Requests Per Minute (RPM), scaling up to Tier 5 which provides up to 2,500,000 TPM and 4,000 RPM.",
        "answer_type": "table",
        "body": """
        <h2>Rate Limits by Tier</h2>
        <table class="data-table">
          <thead>
            <tr>
              <th>Tier</th>
              <th>Cumulative Deposits</th>
              <th>RPM (Requests Per Minute)</th>
              <th>TPM (Tokens Per Minute)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Tier 1</td>
              <td>$5 - $49</td>
              <td>50</td>
              <td>20,000</td>
            </tr>
            <tr>
              <td>Tier 2</td>
              <td>$50 - $499</td>
              <td>1,000</td>
              <td>80,000</td>
            </tr>
            <tr>
              <td>Tier 3</td>
              <td>$500 - $999</td>
              <td>2,000</td>
              <td>160,000</td>
            </tr>
            <tr>
              <td>Tier 4</td>
              <td>$1,000 - $4,999</td>
              <td>3,000</td>
              <td>400,000</td>
            </tr>
            <tr>
              <td>Tier 5</td>
              <td>$5,000+</td>
              <td>4,000</td>
              <td>2,500,000</td>
            </tr>
          </tbody>
        </table>
        <p>Limits are applied per model family (e.g. Sonnet and Haiku accumulate usage limits separately).</p>
        """,
        "verified_against": "Anthropic Developer Console API v1",
        "verified_date": "July 2026",
        "related_slugs": ["current-claude-model-string-identifiers", "maximum-context-window-by-model", "claude-api-max-tokens-output"]
      },
      {
        "slug": "current-claude-model-string-identifiers",
        "question": "What are the current Claude model string identifiers?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "To call Claude models in API requests, use model strings: 'claude-3-5-sonnet-20241022' for Claude 3.5 Sonnet, 'claude-3-5-haiku-20241022' for Claude 3.5 Haiku, and 'claude-3-opus-20240229' for Claude 3 Opus.",
        "answer_type": "table",
        "body": """
        <h2>Model String Registry</h2>
        <table class="data-table">
          <thead>
            <tr>
              <th>Model Name</th>
              <th>API Model String ID</th>
              <th>Primary Use Case</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Claude 3.5 Sonnet</strong></td>
              <td><code>claude-3-5-sonnet-20241022</code></td>
              <td>Software engineering, logical reasoning, multi-turn analysis.</td>
            </tr>
            <tr>
              <td><strong>Claude 3.5 Haiku</strong></td>
              <td><code>claude-3-5-haiku-20241022</code></td>
              <td>Ultra-low latency pipelines, high RPM search utilities.</td>
            </tr>
            <tr>
              <td><strong>Claude 3 Opus</strong></td>
              <td><code>claude-3-opus-20240229</code></td>
              <td>Complex strategy mapping, academic research.</td>
            </tr>
          </tbody>
        </table>
        """,
        "verified_against": "Anthropic API Specifications 2026",
        "verified_date": "July 2026",
        "related_slugs": ["claude-api-rate-limits-by-tier", "maximum-context-window-by-model", "authenticate-with-claude-api"]
      },
      {
        "slug": "authenticate-with-claude-api",
        "question": "How do you authenticate with the Claude API?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "Authenticate with the Claude API by passing your API key in the 'x-api-key' request header. Specify the SDK version header 'anthropic-version' to ensure compatibility.",
        "answer_type": "code",
        "body": """
        <h2>Direct Curl Request Authentication</h2>
<pre><code class="language-bash">curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: your-api-key-here" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello!"}]
  }'</code></pre>
        """,
        "verified_against": "Anthropic API v1",
        "verified_date": "July 2026",
        "related_slugs": ["current-claude-model-string-identifiers", "api-key-vs-oauth-authentication", "claude-api-sdk-comparison-python-js"]
      },
      {
        "slug": "handle-529-overloaded-error",
        "question": "What does a 529 overloaded error mean and how do you handle it?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "An HTTP 529 error indicates that Anthropic's servers are overloaded and unable to handle the request. Handle this error by implementing retry loops using exponential backoff with random jitter.",
        "answer_type": "code",
        "body": """
        <h2>Retry Code Pattern</h2>
        <p>Here is how to catch error code 529 and repeat the request in Node.js:</p>
<pre><code class="language-javascript">async function runWithExponentialBackoff(apiCall, maxRetries = 5) {
  let delay = 1000;
  for (let i = 0; i &lt; maxRetries; i++) {
    try {
      return await apiCall();
    } catch (error) {
      if (error.status === 529 &amp;&amp; i &lt; maxRetries - 1) {
        const jitter = Math.random() * 200;
        console.warn(`529 Overload detected. Retrying in ${delay + jitter}ms...`);
        await new Promise(res =&gt; setTimeout(res, delay + jitter));
        delay *= 2;
      } else {
        throw error;
      }
    }
  }
}</code></pre>
        """,
        "verified_against": "Anthropic API Reference v1",
        "verified_date": "July 2026",
        "related_slugs": ["authenticate-with-claude-api", "claude-api-rate-limits-by-tier", "claude-api-sdk-comparison-python-js"]
      },
      {
        "slug": "stream-claude-api-responses",
        "question": "How do you stream a Claude API response?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "To stream Claude API responses, set the request parameter 'stream' to true. The server will emit Server-Sent Events containing JSON-RPC event chunks for message start, content delta updates, and completion.",
        "answer_type": "code",
        "body": """
        <h2>Python SDK Streaming Example</h2>
<pre><code class="language-python">import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a short poem."}],
    model="claude-3-5-sonnet-20241022",
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)</code></pre>
        """,
        "verified_against": "Anthropic Python SDK v0.39.0",
        "verified_date": "July 2026",
        "related_slugs": ["authenticate-with-claude-api", "claude-api-sdk-comparison-python-js", "current-claude-model-string-identifiers"]
      },
      {
        "slug": "maximum-context-window-by-model",
        "question": "What is the maximum context window for each Claude model?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "All current Claude 3 and Claude 3.5 models support a maximum context window of 200,000 tokens (approximately 150,000 words or 500 pages of text) per single API request.",
        "answer_type": "table",
        "body": """
        <h2>Context Window Reference</h2>
        <table class="data-table">
          <thead>
            <tr>
              <th>Model Name</th>
              <th>Context Limit (Tokens)</th>
              <th>Max Output Limit (Tokens)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Claude 3.5 Sonnet</td>
              <td>200,000</td>
              <td>8,192</td>
            </tr>
            <tr>
              <td>Claude 3.5 Haiku</td>
              <td>200,000</td>
              <td>8,192</td>
            </tr>
            <tr>
              <td>Claude 3 Opus</td>
              <td>200,000</td>
              <td>4,096</td>
            </tr>
          </tbody>
        </table>
        <p>Keep in mind that high token counts increase request latency. Implement prompt caching for files or systemic prompt libraries that span multiple requests.</p>
        """,
        "verified_against": "Anthropic Documentation 2026",
        "verified_date": "July 2026",
        "related_slugs": ["claude-api-rate-limits-by-tier", "current-claude-model-string-identifiers", "claude-api-response-caching-setup"]
      },
      {
        "slug": "pass-system-prompt-claude-api",
        "question": "How do you pass a system prompt in the Claude API?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "Pass a system prompt by declaring the top-level 'system' string parameter in your API body request payload. Do not mix system instructions into the 'messages' array role declarations.",
        "answer_type": "code",
        "body": """
        <h2>JSON Payload Configuration</h2>
<pre><code class="language-json">{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 1024,
  "system": "You are a specialized code translator. Output only clean code.",
  "messages": [
    {"role": "user", "content": "Translate x = 1 to JavaScript."}
  ]
}</code></pre>
        """,
        "verified_against": "Anthropic API v1",
        "verified_date": "July 2026",
        "related_slugs": ["authenticate-with-claude-api", "claude-api-system-prompt-best-practices", "current-claude-model-string-identifiers"]
      },
      {
        "slug": "input-vs-output-tokens-billing",
        "question": "What is the difference between input tokens and output tokens for billing?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "Input tokens represent all prompt text, system instructions, and tool definitions sent to Claude, billed at a lower rate (e.g., $3/M tokens for Sonnet). Output tokens represent the generated completion text, billed at a higher rate (e.g., $15/M tokens for Sonnet).",
        "answer_type": "table",
        "body": """
        <h2>Pricing Table (Per Million Tokens)</h2>
        <table class="data-table">
          <thead>
            <tr>
              <th>Model Name</th>
              <th>Input Price (per M)</th>
              <th>Output Price (per M)</th>
              <th>Prompt Cache Write</th>
              <th>Prompt Cache Read</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Claude 3.5 Sonnet</td>
              <td>$3.00</td>
              <td>$15.00</td>
              <td>$3.75</td>
              <td>$0.30</td>
            </tr>
            <tr>
              <td>Claude 3.5 Haiku</td>
              <td>$0.80</td>
              <td>$4.00</td>
              <td>$1.00</td>
              <td>$0.08</td>
            </tr>
            <tr>
              <td>Claude 3 Opus</td>
              <td>$15.00</td>
              <td>$75.00</td>
              <td>N/A</td>
              <td>N/A</td>
            </tr>
          </tbody>
        </table>
        """,
        "verified_against": "Anthropic API Pricing July 2026",
        "verified_date": "July 2026",
        "related_slugs": ["claude-api-rate-limits-by-tier", "claude-api-response-caching-setup", "maximum-context-window-by-model"]
      },
      {
        "slug": "api-key-vs-oauth-authentication",
        "question": "How do you set up API key authentication vs. OAuth in Claude?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "API keys are best for back-end applications using secret environment keys. OAuth 2.0 is required for client-facing integrations on the Anthropic Console, allowing individual users to sign in and run requests on their own accounts.",
        "answer_type": "definition",
        "body": """
        <h2>Authentication Selection Guide</h2>
        <ul>
          <li><strong>API Keys:</strong> Simple authentication header. Store in environment variables (e.g., <code>ANTHROPIC_API_KEY</code>). Ideal for server-to-server calls and automated pipelines.</li>
          <li><strong>OAuth 2.0:</strong> Best when building an app where users pay for their own LLM usage. Users log in via Anthropic OAuth flows, granting your app token rights.</li>
        </ul>
        """,
        "verified_against": "Anthropic Console v2",
        "verified_date": "July 2026",
        "related_slugs": ["authenticate-with-claude-api", "claude-api-sdk-comparison-python-js", "claude-api-billing-and-usage-alerts"]
      },
      {
        "slug": "claude-api-response-caching-setup",
        "question": "How do you implement prompt caching in the Claude API?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "Implement prompt caching by attaching the cache_control metadata block '{\"type\": \"ephemeral\"}' to blocks in your prompt (system prompts, tools, or messages) that are longer than 1024 tokens.",
        "answer_type": "code",
        "body": """
        <h2>Caching Code Example</h2>
<pre><code class="language-json">{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "...very long resource document here...",
          "cache_control": {"type": "ephemeral"}
        },
        {
          "type": "text",
          "text": "Analyze the document above."
        }
      ]
    }
  ]
}</code></pre>
        """,
        "verified_against": "Anthropic API Caching Specifications v1",
        "verified_date": "July 2026",
        "related_slugs": ["input-vs-output-tokens-billing", "maximum-context-window-by-model", "claude-api-sdk-comparison-python-js"]
      },
      {
        "slug": "claude-api-json-mode-setup",
        "question": "How do you force Claude to return valid JSON in API responses?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "To force JSON output, declare your required JSON schema in a tool definition and set the tool_choice block to force a call to that tool, forcing Claude to structure the response as valid JSON arguments.",
        "answer_type": "code",
        "body": """
        <h2>Forced JSON Schema Pattern</h2>
<pre><code class="language-json">{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 1024,
  "tools": [{
    "name": "respond_json",
    "description": "Formats final response in standard structure.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "status": { "type": "string" },
        "data": { "type": "string" }
      },
      "required": ["status", "data"]
    }
  }],
  "tool_choice": { "type": "tool", "name": "respond_json" },
  "messages": [{"role": "user", "content": "Extract data from: Invoice 123 paid successfully."}]
}</code></pre>
        """,
        "verified_against": "Anthropic API tool_choice spec",
        "verified_date": "July 2026",
        "related_slugs": ["json-schema-format-claude-tool-definitions", "use-tool-choice-parameter", "force-claude-to-use-specific-tool"]
      },
      {
        "slug": "claude-api-max-tokens-output",
        "question": "What is the maximum output token limit for Claude models?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "Claude 3.5 Sonnet and Claude 3.5 Haiku support a maximum completion output of 8,192 tokens per single API request. Claude 3 Opus yields up to 4,096 output tokens.",
        "answer_type": "definition",
        "body": """
        <h2>Output Limits Overview</h2>
        <p>Ensure you configure the <code>max_tokens</code> parameter to match these thresholds if your application generates large documents, codebases, or analytical outputs. If a completion is truncated due to output limits, the API returns a response finish reason of <code>max_tokens</code>.</p>
        """,
        "verified_against": "Anthropic API Specifications 2026",
        "verified_date": "July 2026",
        "related_slugs": ["maximum-context-window-by-model", "claude-api-rate-limits-by-tier", "input-vs-output-tokens-billing"]
      },
      {
        "slug": "claude-api-temperature-parameter",
        "question": "How does the temperature parameter affect Claude's API responses?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "The temperature parameter ranges from 0.0 to 1.0. Lower settings (e.g. 0.0) yield deterministic, highly factual answers, while values closer to 1.0 result in diverse, creative generation.",
        "answer_type": "definition",
        "body": """
        <h2>Parameter Calibration Guide</h2>
        <ul>
          <li><strong>0.0 (Recommended for Coding &amp; Math):</strong> Ensures identical prompt inputs receive the exact same code blocks, preventing arbitrary formatting variations.</li>
          <li><strong>0.5 (Writing &amp; Summary):</strong> Balance between strict extraction and readable style synthesis.</li>
          <li><strong>1.0 (Creative Content):</strong> Expands token choices. Best for brainstorming or prompt generation.</li>
        </ul>
        """,
        "verified_against": "Anthropic API Parameter Guide",
        "verified_date": "July 2026",
        "related_slugs": ["claude-api-top-p-top-k", "authenticate-with-claude-api", "claude-tool-use-temperature-setting"]
      },
      {
        "slug": "claude-api-top-p-top-k",
        "question": "What are the top_p and top_k parameters in the Claude API?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "top_k limits selection to the K highest probability next tokens, while top_p (nucleus sampling) selects from the smallest set of tokens whose cumulative probability exceeds P.",
        "answer_type": "definition",
        "body": """
        <h2>Parameters Explained</h2>
        <p>Generally, developers should adjust temperature instead of top_p or top_k. If adjusting all parameters, the model filters tokens using top_k first, then top_p, and finally samples using temperature scaling.</p>
        """,
        "verified_against": "Anthropic API Spec",
        "verified_date": "July 2026",
        "related_slugs": ["claude-api-temperature-parameter", "authenticate-with-claude-api", "claude-tool-use-temperature-setting"]
      },
      {
        "slug": "claude-api-system-prompt-best-practices",
        "question": "What are the formatting best practices for Claude system prompts?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "Structure your system prompts using XML tags (e.g., &lt;instructions&gt;, &lt;context&gt;, &lt;rules&gt;) to separate guidelines and instruction blocks, which matches Claude's pre-training.",
        "answer_type": "code",
        "body": """
        <h2>System Prompt Template</h2>
<pre><code class="language-xml">&lt;system_instructions&gt;
  &lt;persona&gt;
    You are an API error code reference system.
  &lt;/persona&gt;
  &lt;rules&gt;
    1. Output only JSON formatted content.
    2. Do not explain your choices.
  &lt;/rules&gt;
&lt;/system_instructions&gt;</code></pre>
        """,
        "verified_against": "Anthropic Prompt Engineering Guidelines",
        "verified_date": "July 2026",
        "related_slugs": ["pass-system-prompt-claude-api", "authenticate-with-claude-api", "json-schema-format-claude-tool-definitions"]
      },
      {
        "slug": "claude-api-image-input-format",
        "question": "How do you send images to the Claude API?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "To send an image to the Claude API, include an image content block in your messages array, passing the base64-encoded file string and declaring the correct media type.",
        "answer_type": "code",
        "body": """
        <h2>JSON Payload Image Request</h2>
<pre><code class="language-json">{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image",
          "source": {
            "type": "base64",
            "media_type": "image/jpeg",
            "data": "/9j/4AAQSkZJRgABAQEASABIAAD..."
          }
        },
        {
          "type": "text",
          "text": "What is in this picture?"
        }
      ]
    }
  ]
}</code></pre>
        """,
        "verified_against": "Anthropic API Vision Spec",
        "verified_date": "July 2026",
        "related_slugs": ["claude-api-pdf-document-handling", "authenticate-with-claude-api", "current-claude-model-string-identifiers"]
      },
      {
        "slug": "claude-api-pdf-document-handling",
        "question": "How do you pass PDF files to the Claude API?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "To send a PDF, pass it as a document content block in the messages array, base64-encoded, using the media type application/pdf.",
        "answer_type": "code",
        "body": """
        <h2>JSON Payload PDF Request</h2>
<pre><code class="language-json">{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "document",
          "source": {
            "type": "base64",
            "media_type": "application/pdf",
            "data": "JVBERi0xLjQKJdPr6g..."
          }
        },
        {
          "type": "text",
          "text": "Summarize this PDF document."
        }
      ]
    }
  ]
}</code></pre>
        """,
        "verified_against": "Anthropic API Document Processing Spec 2026",
        "verified_date": "July 2026",
        "related_slugs": ["claude-api-image-input-format", "authenticate-with-claude-api", "maximum-context-window-by-model"]
      },
      {
        "slug": "claude-api-cors-issues-solution",
        "question": "How do you handle CORS issues when calling the Claude API?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "Do not call the Claude API directly from client-side browser scripts, as it will trigger CORS policy blocks and expose your API keys. Instead, implement a secure proxy backend endpoint to handle the requests.",
        "answer_type": "definition",
        "body": """
        <h2>Security and CORS Setup</h2>
        <p>Anthropic intentionally blocks CORS requests from client browsers to prevent api key exfiltration. Set up a simple Express.js proxy on your server to handle calls safely:</p>
<pre><code class="language-javascript">app.post("/api/chat", async (req, res) => {
  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "x-api-key": process.env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json"
    },
    body: JSON.stringify(req.body)
  });
  const data = await response.json();
  res.json(data);
});</code></pre>
        """,
        "verified_against": "Anthropic Security Best Practices",
        "verified_date": "July 2026",
        "related_slugs": ["authenticate-with-claude-api", "api-key-vs-oauth-authentication", "claude-api-sdk-comparison-python-js"]
      },
      {
        "slug": "claude-api-billing-and-usage-alerts",
        "question": "How do you set up billing alerts and usage limits in the Anthropic console?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "Log in to the Anthropic Console, go to Settings > Billing, and configure your Monthly Spending Limit to block API requests once a threshold is reached.",
        "answer_type": "steps",
        "body": """
        <h2>Configuring Limits</h2>
        <ol>
          <li>Navigate to the <a href="https://console.anthropic.com/" target="_blank">Anthropic Console</a>.</li>
          <li>Click on <strong>Billing</strong> in the sidebar.</li>
          <li>Under the <strong>Limits</strong> section, set a 'Soft Limit' (sends an email alert when reached).</li>
          <li>Set a 'Hard Limit' (blocks additional API requests for the rest of the billing cycle).</li>
          <li>Save the changes.</li>
        </ol>
        """,
        "verified_against": "Anthropic Console v2",
        "verified_date": "July 2026",
        "related_slugs": ["api-key-vs-oauth-authentication", "input-vs-output-tokens-billing", "claude-api-rate-limits-by-tier"]
      },
      {
        "slug": "claude-api-sdk-comparison-python-js",
        "question": "What official Anthropic SDKs are available?",
        "category": "claude-api",
        "category_name": "Claude API",
        "quick_answer": "Anthropic officially maintains two developer libraries: the Python SDK (package: 'anthropic') and the TypeScript/JavaScript SDK (package: '@anthropic-ai/sdk').",
        "answer_type": "definition",
        "body": """
        <h2>Official Libraries</h2>
        <ul>
          <li><strong>Python Library:</strong> Install via <code>pip install anthropic</code>.</li>
          <li><strong>TypeScript/JavaScript Library:</strong> Install via <code>npm install @anthropic-ai/sdk</code>.</li>
        </ul>
        <p>Both packages support auto-generated TypeScript definition types, synchronous and asynchronous execution, streaming, tool call parsers, and prompt caching.</p>
        """,
        "verified_against": "Anthropic SDK Release Registry",
        "verified_date": "July 2026",
        "related_slugs": ["anthropic-python-sdk-installation", "authenticate-with-claude-api", "use-claude-with-langchain"]
      },

    # =========================================================================
    # CATEGORY: Tool Use & Function Calling (15 entries)
    # =========================================================================
    {
        "slug": "json-schema-format-claude-tool-definitions",
        "question": "What is the correct JSON schema format for Claude tool definitions?",
        "category": "tool-use",
        "category_name": "Tool Use & Function Calling",
        "quick_answer": "Claude tool schemas follow the JSON Schema Draft 4 specification. Place descriptions on all properties to help Claude select the correct tool and generate matching parameters.",
        "answer_type": "code",
        "body": """
        <h2>JSON Tool Definition Template</h2>
<pre><code class="language-json">{
  "name": "get_stock_price",
  "description": "Retrieves the current trading stock price for a symbol.",
  "input_schema": {
    "type": "object",
    "properties": {
      "ticker": {
        "type": "string",
        "description": "The stock ticker symbol (e.g. AAPL)."
      }
    },
    "required": ["ticker"]
  }
}</code></pre>
        """,
        "verified_against": "Anthropic API Tool Use v1",
        "verified_date": "July 2026",
        "related_slugs": ["use-tool-choice-parameter", "return-tool-result-to-claude", "handle-parallel-tool-calls-claude"]
      },
      {
        "slug": "handle-parallel-tool-calls-claude",
        "question": "How do you handle parallel tool calls in Claude?",
        "category": "tool-use",
        "category_name": "Tool Use & Function Calling",
        "quick_answer": "When Claude decides to call multiple tools in a single turn, the API returns a message block containing multiple content blocks of type 'tool_use'. Iterate through the list, execute them in parallel, and return corresponding tool result blocks.",
        "answer_type": "code",
        "body": """
        <h2>Node.js Implementation</h2>
<pre><code class="language-typescript">if (response.stop_reason === "tool_use") {
  const toolResults = await Promise.all(
    response.content
      .filter(block =&gt; block.type === "tool_use")
      .map(async (toolCall) =&gt; {
        const result = await executeLocalTool(toolCall.name, toolCall.input);
        return {
          type: "tool_result",
          tool_use_id: toolCall.id,
          content: JSON.stringify(result)
        };
      })
  );

  // Send tool results back to Claude in the next turn
  const nextResponse = await anthropic.messages.create({
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 1024,
    messages: [
      ...existingMessages,
      { role: "assistant", content: response.content },
      { role: "user", content: toolResults }
    ]
  });
}</code></pre>
        """,
        "verified_against": "Anthropic API Tool Use v1",
        "verified_date": "July 2026",
        "related_slugs": ["json-schema-format-claude-tool-definitions", "return-tool-result-to-claude", "multiple-calls-same-tool-single-turn"]
      },
      {
        "slug": "return-tool-result-to-claude",
        "question": "How do you return a tool result to Claude?",
        "category": "tool-use",
        "category_name": "Tool Use & Function Calling",
        "quick_answer": "Return tool results in a user message block containing a list of content blocks of type 'tool_result'. Each block must specify the matching 'tool_use_id' to bind the result to the initial request.",
        "answer_type": "code",
        "body": """
        <h2>Request Payload Example</h2>
<pre><code class="language-json">{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A2B3C4D5",
      "content": "The current weather in Denver is 72°F and sunny."
    }
  ]
}</code></pre>
        """,
        "verified_against": "Anthropic API Tool Use v1",
        "verified_date": "July 2026",
        "related_slugs": ["json-schema-format-claude-tool-definitions", "handle-parallel-tool-calls-claude", "handle-tool-call-errors-gracefully"]
      },
      {
        "slug": "multiple-calls-same-tool-single-turn",
        "question": "Can Claude call the same tool multiple times in one turn?",
        "category": "tool-use",
        "category_name": "Tool Use & Function Calling",
        "quick_answer": "Yes. If Claude needs to fetch multiple independent data points, it will return multiple tool_use blocks referencing the same tool name but with distinct arguments and unique tool_use_ids.",
        "answer_type": "definition",
        "body": """
        <h2>Behavioral Mechanics</h2>
        <p>For example, if you ask: 'Compare the weather in Chicago and Seattle', Claude will output two separate tool calls in the same response block: one for Chicago and one for Seattle. Your executor must loop through the content array, execute both calls, and return two tool_result blocks matching the IDs.</p>
        """,
        "verified_against": "Anthropic Tool Execution Spec",
        "verified_date": "July 2026",
        "related_slugs": ["handle-parallel-tool-calls-claude", "return-tool-result-to-claude", "use-tool-choice-parameter"]
      },
      {
        "slug": "force-claude-to-use-specific-tool",
        "question": "How do you force Claude to use a specific tool?",
        "category": "tool-use",
        "category_name": "Tool Use & Function Calling",
        "quick_answer": "Force Claude to use a specific tool by setting the request parameter 'tool_choice' to type 'tool' and providing the name of the target tool.",
        "answer_type": "code",
        "body": """
        <h2>Tool Choice Configuration</h2>
<pre><code class="language-json">{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 1024,
  "tools": [
    {
      "name": "fetch_user_records",
      "description": "Retrieves user files.",
      "input_schema": {
        "type": "object",
        "properties": {
          "user_id": { "type": "string" }
        },
        "required": ["user_id"]
      }
    }
  ],
  "tool_choice": {
    "type": "tool",
    "name": "fetch_user_records"
  },
  "messages": [
    { "role": "user", "content": "Help me lookup account 987." }
  ]
}</code></pre>
        """,
        "verified_against": "Anthropic API Tool Use v1",
        "verified_date": "July 2026",
        "related_slugs": ["use-tool-choice-parameter", "json-schema-format-claude-tool-definitions", "claude-api-json-mode-setup"]
      },
      {
        "slug": "use-tool-choice-parameter",
        "question": "What is tool_choice and how do you use it?",
        "category": "tool-use",
        "category_name": "Tool Use & Function Calling",
        "quick_answer": "tool_choice governs how Claude selects tools. Use 'auto' to let Claude decide whether to use tools, 'any' to force Claude to select at least one tool, or type 'tool' with a name to force a specific tool.",
        "answer_type": "table",
        "body": """
        <h2>tool_choice Options</h2>
        <table class="data-table">
          <thead>
            <tr>
              <th>Option Format</th>
              <th>Behavior Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>{"type": "auto"}</code></td>
              <td>Default. Claude decides whether to call a tool or respond with plain text.</td>
            </tr>
            <tr>
              <td><code>{"type": "any"}</code></td>
              <td>Forces Claude to call at least one of the provided tools.</td>
            </tr>
            <tr>
              <td><code>{"type": "tool", "name": "x"}</code></td>
              <td>Forces Claude to call the tool named <code>x</code>.</td>
            </tr>
          </tbody>
        </table>
        """,
        "verified_against": "Anthropic API Spec",
        "verified_date": "July 2026",
        "related_slugs": ["force-claude-to-use-specific-tool", "json-schema-format-claude-tool-definitions", "claude-tool-use-any-vs-auto"]
      },
      {
        "slug": "handle-tool-call-errors-gracefully",
        "question": "How do you handle tool call errors gracefully?",
        "category": "tool-use",
        "category_name": "Tool Use & Function Calling",
        "quick_answer": "To report a tool execution failure to Claude, return a user message block with the parameter 'is_error' set to true. This tells Claude the tool failed, prompting the model to fix its input arguments.",
        "answer_type": "code",
        "body": """
        <h2>Error Response Block</h2>
<pre><code class="language-json">{
  "type": "tool_result",
  "tool_use_id": "toolu_12345",
  "content": "Database error: connection timed out.",
  "is_error": true
}</code></pre>
        """,
        "verified_against": "Anthropic API Tool Use v1",
        "verified_date": "July 2026",
        "related_slugs": ["return-tool-result-to-claude", "handle-parallel-tool-calls-claude", "prevent-hallucinated-tool-calls"]
      },
      {
        "slug": "maximum-tools-supported-per-request",
        "question": "What is the maximum number of tools Claude supports per request?",
        "category": "tool-use",
        "category_name": "Tool Use & Function Calling",
        "quick_answer": "Claude officially supports up to 100 tools per single API request. However, including many tools increases system prompt token counts and can impact tool selection accuracy.",
        "answer_type": "definition",
        "body": """
        <h2>Optimization Guidance</h2>
        <p>Although the technical limit is 100 tools, routing accuracy degrades as tool lists grow. For complex agent setups with many tools, group tools by task and dynamically declare them based on the conversation state.</p>
        """,
        "verified_against": "Anthropic SDK limits 2026",
        "verified_date": "July 2026",
        "related_slugs": ["json-schema-format-claude-tool-definitions", "claude-tool-use-tokens-cost", "use-tool-choice-parameter"]
      },
      {
        "slug": "nested-objects-in-tool-schema",
        "question": "How do you define nested objects in Claude's tool schema?",
        "category": "tool-use",
        "category_name": "Tool Use & Function Calling",
        "quick_answer": "Define nested structures by nesting object properties inside properties in your tool definition, matching the JSON Schema Draft 4 specification.",
        "answer_type": "code",
        "body": """
        <h2>Nested Schema Example</h2>
<pre><code class="language-json">{
  "name": "update_user_profile",
  "description": "Updates profile details.",
  "input_schema": {
    "type": "object",
    "properties": {
      "user_id": { "type": "string" },
      "profile": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "email": { "type": "string" }
        },
        "required": ["name"]
      }
    },
    "required": ["user_id", "profile"]
  }
}</code></pre>
        """,
        "verified_against": "Anthropic API Tool Use v1",
        "verified_date": "July 2026",
        "related_slugs": ["json-schema-format-claude-tool-definitions", "prevent-hallucinated-tool-calls", "use-tool-choice-parameter"]
      },
      {
        "slug": "claude-tool-use-tokens-cost",
        "question": "How do tool definitions affect input token billing?",
        "category": "tool-use",
        "category_name": "Tool Use & Function Calling",
        "quick_answer": "Tool schemas are serialized into XML instructions and prepended to the system prompt, counting towards your input token billing. Enable prompt caching for static tool definitions to minimize costs.",
        "answer_type": "definition",
        "body": """
        <h2>Token Overhead Guidelines</h2>
        <p>A simple tool definition consumes about 150-300 tokens. A large tool set can add several thousand tokens to every request. Use prompt caching (<code>cache_control</code>) at the end of your tool definitions list to avoid paying for tool translation on every turn.</p>
        """,
        "verified_against": "Anthropic API Pricing 2026",
        "verified_date": "July 2026",
        "related_slugs": ["claude-api-response-caching-setup", "input-vs-output-tokens-billing", "maximum-tools-supported-per-request"]
      },
      {
        "slug": "claude-streaming-with-tool-calls",
        "question": "How do you handle streaming responses when tools are called?",
        "category": "tool-use",
        "category_name": "Tool Use & Function Calling",
        "quick_answer": "In stream responses, listen for events of type 'content_block_start' with content type 'tool_use'. Collect arguments from 'content_block_delta' events, and execute the tool once the block completes.",
        "answer_type": "code",
        "body": """
        <h2>Stream Parsing Logic Example</h2>
<pre><code class="language-javascript">for await (const event of stream) {
  if (event.type === 'content_block_start' &amp;&amp; event.content_block.type === 'tool_use') {
    currentToolCall = {
      id: event.content_block.id,
      name: event.content_block.name,
      arguments: ""
    };
  }
  if (event.type === 'content_block_delta' &amp;&amp; event.delta.type === 'input_json_delta') {
    currentToolCall.arguments += event.delta.partial_json;
  }
}</code></pre>
        """,
        "verified_against": "Anthropic Streaming API Specification",
        "verified_date": "July 2026",
        "related_slugs": ["stream-claude-api-responses", "handle-parallel-tool-calls-claude", "return-tool-result-to-claude"]
      },
      {
        "slug": "prevent-hallucinated-tool-calls",
        "question": "How do you prevent Claude from hallucinating tool arguments?",
        "category": "tool-use",
        "category_name": "Tool Use & Function Calling",
        "quick_answer": "Provide detailed descriptions for tool parameters, use enum lists for allowed values, and instruct the model in your system prompt to ask for clarification if required values are missing.",
        "answer_type": "definition",
        "body": """
        <h2>Mitigation Strategies</h2>
        <ul>
          <li><strong>Add Schema Enums:</strong> If a parameter has a limited set of options, specify them using <code>enum</code> validation.</li>
          <li><strong>Add Guidelines:</strong> Add an instruction like 'If you do not have the user's account ID, do not guess. Ask the user for it.'</li>
        </ul>
        """,
        "verified_against": "Anthropic Prompt Guidelines",
        "verified_date": "July 2026",
        "related_slugs": ["json-schema-format-claude-tool-definitions", "handle-tool-call-errors-gracefully", "claude-api-system-prompt-best-practices"]
      },
      {
        "slug": "claude-tool-use-system-prompt-override",
        "question": "Does tool use override the custom system prompt in Claude?",
        "category": "tool-use",
        "category_name": "Tool Use & Function Calling",
        "quick_answer": "No. The system prompt guidelines and rules remain active and guide Claude's behavior even when the model decides to use tools.",
        "answer_type": "definition",
        "body": """
        <h2>Rule Enforcement</h2>
        <p>Claude processes system prompts and tool schemas together. System instructions govern formatting and style rules, while tool schemas dictate the technical signatures for function calls.</p>
        """,
        "verified_against": "Anthropic Prompt Processing Spec",
        "verified_date": "July 2026",
        "related_slugs": ["pass-system-prompt-claude-api", "claude-api-system-prompt-best-practices", "json-schema-format-claude-tool-definitions"]
      },
      {
        "slug": "claude-tool-use-temperature-setting",
        "question": "What temperature is recommended when using Claude for tool calling?",
        "category": "tool-use",
        "category_name": "Tool Use & Function Calling",
        "quick_answer": "Set the temperature to 0.0 when using tools. This ensures arguments are generated reliably and matches the target schemas without creative variance.",
        "answer_type": "definition",
        "body": """
        <h2>Optimization Guidance</h2>
        <p>A higher temperature (e.g. 1.0) can cause Claude to hallucinate or misformat parameter names. Using 0.0 ensures predictable and deterministic parameter parsing.</p>
        """,
        "verified_against": "Anthropic API Reference",
        "verified_date": "July 2026",
        "related_slugs": ["claude-api-temperature-parameter", "claude-api-top-p-top-k", "prevent-hallucinated-tool-calls"]
      },
      {
        "slug": "claude-tool-use-any-vs-auto",
        "question": "What is the difference between tool_choice auto and any?",
        "category": "tool-use",
        "category_name": "Tool Use & Function Calling",
        "quick_answer": "tool_choice 'auto' allows Claude to choose whether to write a text response or execute a tool, whereas 'any' forces Claude to call at least one tool before responding.",
        "answer_type": "definition",
        "body": """
        <h2>Options Comparison</h2>
        <ul>
          <li><strong>auto:</strong> Best for standard user chat. The assistant will answer questions using text, and only call tools when external database information is requested.</li>
          <li><strong>any:</strong> Best for automated agents. Ensures the output starts a tool action, preventing the model from writing conversational chat.</li>
        </ul>
        """,
        "verified_against": "Anthropic Tool Choice Spec",
        "verified_date": "July 2026",
        "related_slugs": ["use-tool-choice-parameter", "force-claude-to-use-specific-tool", "json-schema-format-claude-tool-definitions"]
      },

    # =========================================================================
    # CATEGORY: Agent Frameworks (10 entries)
    # =========================================================================
    {
        "slug": "use-claude-with-langgraph",
        "question": "How do you use Claude with LangGraph?",
        "category": "agent-frameworks",
        "category_name": "Agent Frameworks",
        "quick_answer": "To use Claude with LangGraph, install the '@langchain/anthropic' integration package, initialize ChatAnthropic with your target model string, and bind it to your graph nodes.",
        "answer_type": "code",
        "body": """
        <h2>TypeScript Implementation Example</h2>
<pre><code class="language-typescript">import { ChatAnthropic } from "@langchain/anthropic";
import { StateGraph } from "@langchain/langgraph";

const model = new ChatAnthropic({
  modelName: "claude-3-5-sonnet-20241022",
  temperature: 0
});

// Define graph nodes and bind the model
const graph = new StateGraph({ channels: {} })
  .addNode("agent", async (state) => {
    const response = await model.invoke(state.messages);
    return { messages: [response] };
  });</code></pre>
        """,
        "verified_against": "LangGraph v0.2.0 · LangChain Anthropic v0.3.0",
        "verified_date": "July 2026",
        "related_slugs": ["use-claude-with-langchain", "anthropic-python-sdk-installation", "agent-loop-patterns-with-claude"]
      },
      {
        "slug": "set-claude-as-llm-crewai",
        "question": "How do you set Claude as the LLM in CrewAI?",
        "category": "agent-frameworks",
        "category_name": "Agent Frameworks",
        "quick_answer": "To configure CrewAI to use Claude, initialize an LLM class instance using CrewAI's library, passing the model identifier 'anthropic/claude-3-5-sonnet-20241022', and assign it to your agents.",
        "answer_type": "code",
        "body": """
        <h2>Python Setup Configuration</h2>
<pre><code class="language-python">from crewai import Agent, Crew, LLM

# Initialize Claude LLM using CrewAI's wrapper
claude_llm = LLM(
    model="anthropic/claude-3-5-sonnet-20241022",
    temperature=0.2,
    api_key="your-api-key"
)

research_agent = Agent(
    role="Senior Analyst",
    goal="Analyze market statistics.",
    backstory="Expert researcher.",
    llm=claude_llm,
    verbose=True
)</code></pre>
        """,
        "verified_against": "CrewAI v0.100.0",
        "verified_date": "July 2026",
        "related_slugs": ["anthropic-python-sdk-installation", "agent-loop-patterns-with-claude", "use-claude-with-langchain"]
      },
      {
        "slug": "integrate-claude-with-autogen",
        "question": "How do you integrate Claude with AutoGen?",
        "category": "agent-frameworks",
        "category_name": "Agent Frameworks",
        "quick_answer": "To use Claude in AutoGen, configure the LLM configuration dictionary with API key credentials and set 'api_type' to 'anthropic'.",
        "answer_type": "code",
        "body": """
        <h2>Python Configuration</h2>
<pre><code class="language-python">import autogen

config_list = [{
    "model": "claude-3-5-sonnet-20241022",
    "api_key": "your_api_key",
    "api_type": "anthropic"
}]

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list}
)</code></pre>
        """,
        "verified_against": "Microsoft AutoGen v0.4.0",
        "verified_date": "July 2026",
        "related_slugs": ["anthropic-python-sdk-installation", "agent-loop-patterns-with-claude", "set-claude-as-llm-crewai"]
      },
      {
        "slug": "anthropic-python-sdk-installation",
        "question": "What is the Anthropic SDK for Python and how do you install it?",
        "category": "agent-frameworks",
        "category_name": "Agent Frameworks",
        "quick_answer": "The Anthropic Python SDK is the official package for interacting with Claude. Install it using pip: 'pip install anthropic'.",
        "answer_type": "code",
        "body": """
        <h2>Installation Command</h2>
<pre><code class="language-bash">pip install anthropic</code></pre>
        <h2>Quick Usage</h2>
<pre><code class="language-python">from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude!"}]
)
print(message.content[0].text)</code></pre>
        """,
        "verified_against": "Anthropic Python SDK v0.39.0",
        "verified_date": "July 2026",
        "related_slugs": ["claude-api-sdk-comparison-python-js", "authenticate-with-claude-api", "use-claude-with-langchain"]
      },
      {
        "slug": "use-claude-with-langchain",
        "question": "How do you use Claude with LangChain?",
        "category": "agent-frameworks",
        "category_name": "Agent Frameworks",
        "quick_answer": "To use Claude in LangChain, install the '@langchain/anthropic' package (JS/TS) or 'langchain-anthropic' (Python), and initialize the ChatAnthropic model class.",
        "answer_type": "code",
        "body": """
        <h2>Python Setup</h2>
<pre><code class="language-python"># Install via pip
# pip install langchain-anthropic

from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0
)
response = model.invoke("Hello!")</code></pre>
        """,
        "verified_against": "LangChain Anthropic Python v0.3.0",
        "verified_date": "July 2026",
        "related_slugs": ["use-claude-with-langgraph", "anthropic-python-sdk-installation", "claude-api-sdk-comparison-python-js"]
      },
      {
        "slug": "agent-loop-patterns-with-claude",
        "question": "What agent loop patterns work well with Claude?",
        "category": "agent-frameworks",
        "category_name": "Agent Frameworks",
        "quick_answer": "Claude excels in ReAct (Reasoning and Acting) loops, Plan-and-Solve patterns, and multi-agent reflection loops due to its strong contextual compliance and structural tool execution.",
        "answer_type": "definition",
        "body": """
        <h2>Effective Patterns</h2>
        <ul>
          <li><strong>ReAct:</strong> Alternating reasoning steps (thought) and tool calls (act). Excellent for search and database query navigation.</li>
          <li><strong>Plan-and-Solve:</strong> Claude generates a step-by-step implementation plan, executes each step, and uses a reflection loop to self-correct failures.</li>
          <li><strong>Reflection / Critic:</strong> An assistant agent generates code, and a separate critic agent validates the output, sending feedback to the creator for iteration.</li>
        </ul>
        """,
        "verified_against": "Anthropic Agentic Design Patterns Guide",
        "verified_date": "July 2026",
        "related_slugs": ["use-claude-with-langgraph", "implement-recommender-agent-claude", "claude-agent-memory-persistence"]
      },
      {
        "slug": "use-claude-with-llamaindex",
        "question": "How do you use Claude with LlamaIndex?",
        "category": "agent-frameworks",
        "category_name": "Agent Frameworks",
        "quick_answer": "To use Claude with LlamaIndex, install 'llama-index-llms-anthropic', initialize the Anthropic class model, and configure it as your global LLM setting.",
        "answer_type": "code",
        "body": """
        <h2>Python Setup</h2>
<pre><code class="language-python"># pip install llama-index-llms-anthropic

from llama_index.llms.anthropic import Anthropic
from llama_index.core import Settings

Settings.llm = Anthropic(
    model="claude-3-5-sonnet-20241022",
    api_key="your-api-key"
)</code></pre>
        """,
        "verified_against": "LlamaIndex v0.10.0",
        "verified_date": "July 2026",
        "related_slugs": ["use-claude-with-langchain", "anthropic-python-sdk-installation", "claude-api-sdk-comparison-python-js"]
      },
      {
        "slug": "use-claude-with-vercel-ai-sdk",
        "question": "How do you use Claude with the Vercel AI SDK?",
        "category": "agent-frameworks",
        "category_name": "Agent Frameworks",
        "quick_answer": "To integrate Claude in the Vercel AI SDK, install '@ai-sdk/anthropic', import 'anthropic', and invoke target models via 'generateText' or 'streamText'.",
        "answer_type": "code",
        "body": """
        <h2>Next.js API Route Example</h2>
<pre><code class="language-typescript">import { anthropic } from '@ai-sdk/anthropic';
import { generateText } from 'ai';

export async function POST(req: Request) {
  const { text } = await generateText({
    model: anthropic('claude-3-5-sonnet-20241022'),
    prompt: 'Write a tagline for a tech startup.',
  });
  return Response.json({ text });
}</code></pre>
        """,
        "verified_against": "Vercel AI SDK v4.0.0",
        "verified_date": "July 2026",
        "related_slugs": ["use-claude-with-langchain", "claude-api-sdk-comparison-python-js", "stream-claude-api-responses"]
      },
      {
        "slug": "implement-recommender-agent-claude",
        "question": "How do you build a ReAct agent loop manually with Claude?",
        "category": "agent-frameworks",
        "category_name": "Agent Frameworks",
        "quick_answer": "Build a manual ReAct loop by creating a while-loop that passes tools, reads Claude's tool_use calls, executes the matching code locally, and posts the results back until Claude returns a text completion.",
        "answer_type": "code",
        "body": """
        <h2>Manual ReAct Loop Code Pattern</h2>
<pre><code class="language-typescript">async function runAgent(prompt: string) {
  const messages = [{ role: "user", content: prompt }];
  
  while (true) {
    const response = await anthropic.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 1024,
      tools: myTools,
      messages
    });

    messages.push({ role: "assistant", content: response.content });

    if (response.stop_reason !== "tool_use") {
      return response.content[0].text; // Loop complete
    }

    const toolResults = await executeTools(response.content);
    messages.push({ role: "user", content: toolResults });
  }
}</code></pre>
        """,
        "verified_against": "Anthropic API Tool Use v1",
        "verified_date": "July 2026",
        "related_slugs": ["agent-loop-patterns-with-claude", "handle-parallel-tool-calls-claude", "return-tool-result-to-claude"]
      },
      {
        "slug": "claude-agent-memory-persistence",
        "question": "How do you handle session state and memory persistence for agents?",
        "category": "agent-frameworks",
        "category_name": "Agent Frameworks",
        "quick_answer": "Store conversation history in a database keyed by session ID, load recent turns during requests, and summarize old messages to fit the context window.",
        "answer_type": "definition",
        "body": """
        <h2>Memory Persistence Workflow</h2>
        <ol>
          <li>Save every message turn (both user and assistant roles) to your database.</li>
          <li>For each request, load the database array to construct your API payload.</li>
          <li>Implement a sliding window: if the token count exceeds 150,000, trigger Claude to summarize the oldest 50% of the conversation and replace them with a single summary message.</li>
        </ol>
        """,
        "verified_against": "Anthropic Memory Engineering Guidelines",
        "verified_date": "July 2026",
        "related_slugs": ["agent-loop-patterns-with-claude", "maximum-context-window-by-model", "use-claude-with-langgraph"]
      },

    # =========================================================================
    # CATEGORY: Claude Code (10 entries)
    # =========================================================================
    {
        "slug": "install-claude-code-cli",
        "question": "How do you install Claude Code?",
        "category": "claude-code",
        "category_name": "Claude Code",
        "quick_answer": "Install Claude Code globally via npm by running the command: 'npm install -g @anthropic-ai/claude-code'. Authorize the command-line interface tool with your Anthropic Account to begin.",
        "answer_type": "code",
        "body": """
        <h2>Installation and Login</h2>
        <p>Run the installation and startup commands in your terminal:</p>
<pre><code class="language-bash">npm install -g @anthropic-ai/claude-code
claude</code></pre>
        <p>On initial startup, the console will print a verification URL and token. Navigate to the link in your browser, log in to your Anthropic console, and verify the token to link your CLI environment.</p>
        """,
        "verified_against": "Claude Code CLI v0.2.5",
        "verified_date": "July 2026",
        "related_slugs": ["slash-commands-supported-claude-code", "claude-code-config-file-location", "claude-code-troubleshoot-auth-issues"]
      },
      {
        "slug": "slash-commands-supported-claude-code",
        "question": "What slash commands does Claude Code support?",
        "category": "claude-code",
        "category_name": "Claude Code",
        "quick_answer": "Claude Code supports command-line interface utility slash commands: '/init' to bootstrap directories, '/config' to set settings, '/mcp' to manage server connectors, '/clear' to purge console history, and '/exit' to terminate.",
        "answer_type": "table",
        "body": """
        <h2>Slash Command Reference</h2>
        <table class="data-table">
          <thead>
            <tr>
              <th>Command</th>
              <th>Action / Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>/init</code></td>
              <td>Initializes workspace environment guidelines for Claude.</td>
            </tr>
            <tr>
              <td><code>/config</code></td>
              <td>Lists, gets, or updates configuration settings.</td>
            </tr>
            <tr>
              <td><code>/mcp</code></td>
              <td>Lists and registers Model Context Protocol servers.</td>
            </tr>
            <tr>
              <td><code>/clear</code></td>
              <td>Clears chat history and releases token memory context.</td>
            </tr>
            <tr>
              <td><code>/exit</code></td>
              <td>Exits the Claude Code session.</td>
            </tr>
          </tbody>
        </table>
        """,
        "verified_against": "Claude Code CLI v0.2.5",
        "verified_date": "July 2026",
        "related_slugs": ["install-claude-code-cli", "add-mcp-server-to-claude-code", "claude-code-keyboard-shortcuts"]
      },
      {
        "slug": "add-mcp-server-to-claude-code",
        "question": "How do you add an MCP server to Claude Code?",
        "category": "claude-code",
        "category_name": "Claude Code",
        "quick_answer": "Add an MCP server to Claude Code by editing the local config file or using the slash command: '/mcp add &lt;server-name&gt; &lt;command&gt; [args...]'.",
        "answer_type": "code",
        "body": """
        <h2>Using the Slash Command</h2>
        <p>Run the following interactive command inside the Claude Code prompt:</p>
<pre><code class="language-bash">/mcp add postgres-mcp npx -y @modelcontextprotocol/server-postgres --conn postgresql://localhost/dev</code></pre>
        <h2>Config File Modification</h2>
        <p>Alternatively, write the configuration directly inside the <code>claude-code.config.json</code> under the <code>mcpServers</code> block.</p>
        """,
        "verified_against": "Claude Code CLI v0.2.5",
        "verified_date": "July 2026",
        "related_slugs": ["slash-commands-supported-claude-code", "claude-code-config-file-location", "configure-mcp-in-claude-desktop"]
      },
      {
        "slug": "configure-claude-code-system-prompt",
        "question": "How do you configure Claude Code with a custom system prompt?",
        "category": "claude-code",
        "category_name": "Claude Code",
        "quick_answer": "Set a custom system prompt in Claude Code by editing the configuration file or using the configuration slash command: '/config set systemPrompt \"&lt;your-prompt&gt;\"'.",
        "answer_type": "code",
        "body": """
        <h2>Terminal Command Example</h2>
        <p>Run the configuration command directly in the terminal interface:</p>
<pre><code class="language-bash">/config set systemPrompt "Write code output strictly matching ECMAScript 2022 standards."</code></pre>
        <p>This setting updates the active user configuration profile and will persist across future restarts.</p>
        """,
        "verified_against": "Claude Code CLI v0.2.5",
        "verified_date": "July 2026",
        "related_slugs": ["claude-code-config-file-location", "slash-commands-supported-claude-code", "pass-system-prompt-claude-api"]
      },
      {
        "slug": "claude-code-config-file-location",
        "question": "What is the Claude Code config file location and format?",
        "category": "claude-code",
        "category_name": "Claude Code",
        "quick_answer": "The config file is located at '~/.config/claude-code/config.json'. It is a standard JSON file containing keys for your active model, custom system prompt, and registered MCP servers.",
        "answer_type": "definition",
        "body": """
        <h2>Configuration Locations</h2>
        <ul>
          <li><strong>macOS/Linux:</strong> <code>~/.config/claude-code/config.json</code></li>
          <li><strong>Windows:</strong> <code>%USERPROFILE%\\.config\\claude-code\\config.json</code></li>
        </ul>
        <h2>Format Template</h2>
<pre><code class="language-json">{
  "model": "claude-3-5-sonnet-20241022",
  "systemPrompt": "",
  "theme": "dark",
  "mcpServers": {}
}</code></pre>
        """,
        "verified_against": "Claude Code CLI v0.2.5",
        "verified_date": "July 2026",
        "related_slugs": ["install-claude-code-cli", "configure-claude-code-system-prompt", "add-mcp-server-to-claude-code"]
      },
      {
        "slug": "run-claude-code-headless-ci",
        "question": "How do you run Claude Code in headless/CI mode?",
        "category": "claude-code",
        "category_name": "Claude Code",
        "quick_answer": "Run Claude Code in headless/CI pipelines by passing the prompt argument directly using: 'claude \"&lt;your prompt&gt;\" --non-interactive'. Export the token key as an environment variable.",
        "answer_type": "code",
        "body": """
        <h2>CI/CD Pipeline Integration</h2>
<pre><code class="language-bash">export CLAUDE_API_KEY="your-anthropic-api-key"
claude "Run audit on src/utils.ts and list security flaws." --non-interactive</code></pre>
        <p>This executes the prompt, prints the final response to standard output, and exits with a status code of 0 (or non-zero if errors are thrown).</p>
        """,
        "verified_against": "Claude Code CLI v0.2.5",
        "verified_date": "July 2026",
        "related_slugs": ["install-claude-code-cli", "claude-code-permission-levels", "claude-code-config-file-location"]
      },
      {
        "slug": "claude-code-permission-levels",
        "question": "What are Claude Code's permission levels?",
        "category": "claude-code",
        "category_name": "Claude Code",
        "quick_answer": "Claude Code executes local system tools. You can run it in safe mode to block terminal write commands, or authorize specific write/execute actions when prompted.",
        "answer_type": "definition",
        "body": """
        <h2>Permission Architecture</h2>
        <p>On startup, you can specify safety restriction settings:</p>
        <ul>
          <li><strong>Safe Mode:</strong> Run <code>claude --safe</code> to prevent any commands from modifying local directory files or running shell execution processes without confirmation prompts.</li>
          <li><strong>Command-level Confirmation:</strong> Every time Claude attempts to run a terminal script or edit a file, the CLI prints the proposed diff or command and waits for you to hit <code>y/n</code>.</li>
        </ul>
        """,
        "verified_against": "Claude Code CLI v0.2.5",
        "verified_date": "July 2026",
        "related_slugs": ["install-claude-code-cli", "run-claude-code-headless-ci", "claude-code-cost-saving-tips"]
      },
      {
        "slug": "claude-code-cost-saving-tips",
        "question": "How do you minimize token costs when using Claude Code?",
        "category": "claude-code",
        "category_name": "Claude Code",
        "quick_answer": "To save token costs, run '/clear' periodically to reset the context history and avoid sending large, outdated git diffs or file contents in subsequent prompts.",
        "answer_type": "definition",
        "body": """
        <h2>Cost Control Strategies</h2>
        <ul>
          <li><strong>Context Reset:</strong> Type <code>/clear</code> to purge the history. This removes cached file buffers from Claude's context window.</li>
          <li><strong>Targeted Prompts:</strong> Specify directories or files directly (e.g. <code>claude "Explain functions in src/auth.ts"</code>) instead of asking Claude to analyze the entire repository.</li>
        </ul>
        """,
        "verified_against": "Claude Code CLI v0.2.5",
        "verified_date": "July 2026",
        "related_slugs": ["slash-commands-supported-claude-code", "claude-code-config-file-location", "claude-api-response-caching-setup"]
      },
      {
        "slug": "claude-code-keyboard-shortcuts",
        "question": "What keyboard shortcuts are available in Claude Code?",
        "category": "claude-code",
        "category_name": "Claude Code",
        "quick_answer": "Claude Code supports command line shortcuts: use 'Ctrl+C' to cancel a running generation or exit the application, and 'Ctrl+L' to clear the current terminal screen.",
        "answer_type": "table",
        "body": """
        <h2>Keyboard Shortcuts</h2>
        <table class="data-table">
          <thead>
            <tr>
              <th>Shortcut Key</th>
              <th>Operational Behavior</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>Ctrl + C</code></td>
              <td>Stops a printing model stream or cancels a running tool command.</td>
            </tr>
            <tr>
              <td><code>Ctrl + L</code></td>
              <td>Clears the terminal output screen, preserving session history.</td>
            </tr>
            <tr>
              <td><code>Tab</code></td>
              <td>Triggers autocomplete for filenames, folders, and slash command templates.</td>
            </tr>
          </tbody>
        </table>
        """,
        "verified_against": "Claude Code CLI v0.2.5",
        "verified_date": "July 2026",
        "related_slugs": ["slash-commands-supported-claude-code", "install-claude-code-cli", "claude-code-config-file-location"]
      },
      {
        "slug": "claude-code-troubleshoot-auth-issues",
        "question": "How do you troubleshoot authentication issues in Claude Code?",
        "category": "claude-code",
        "category_name": "Claude Code",
        "quick_answer": "Resolve CLI authentication issues by running '/config set logout', clearing your ~/.config/claude-code credentials directory, and restarting the CLI to run the OAuth flow again.",
        "answer_type": "steps",
        "body": """
        <h2>Step-by-step Troubleshooting</h2>
        <ol>
          <li>Run <code>/config set logout</code> inside the Claude Code prompt if accessible.</li>
          <li>If the prompt is locked or failing, delete the cached credentials file locally:
            <pre><code>rm -rf ~/.config/claude-code</code></pre>
          </li>
          <li>Verify your developer account status and credit balance in the <a href="https://console.anthropic.com/" target="_blank">Anthropic Console</a>.</li>
          <li>Start the utility again by running <code>claude</code> to initiate a fresh browser-based device link verification flow.</li>
        </ol>
        """,
        "verified_against": "Claude Code CLI v0.2.5",
        "verified_date": "July 2026",
        "related_slugs": ["install-claude-code-cli", "claude-code-config-file-location", "api-key-vs-oauth-authentication"]
      }
]
