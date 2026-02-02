# Project Structure & Architecture

This section explains the project structure and how MCP servers work conceptually.

## Understanding the Luise API

The **Luise API** (hosted at `api.m365princess.com`) is a real FastAPI service with these endpoints:

- **`GET /profile`** - Personal profile with modes: `default`, `conference`, `afterhours`
  - Special unlock code: `unlock=ff69b4` reveals extra fields
- **`GET /profile/quote`** - Get quotes on various topics
- **`GET /skills`** - Technical skills (filterable by `domain`)
- **`GET /talks`** - Speaking engagements (filterable by `year`)
- **`GET /projects`** - Project portfolio 
- **`POST /talks/{id}/questions`** - Submit questions about talks

**📝 Note:** While we use the Luise API as our example, you can easily adapt this tutorial to work with **any REST API** - your own personal API, company internal services, public APIs like GitHub or weather services, or any other HTTP-based data source. The patterns and code structure remain the same!

## MCP Server Architecture

```
[AI Assistant] ←→ [MCP Server] ←→ [Luise API]
     ↑               ↑               ↑
  GitHub Copilot   mcp_server.py   api.m365princess.com
```

Each API endpoint becomes an **MCP Tool** that AI assistants can use naturally in conversation.

## Project Structure

Here's exactly what we'll build:

```
luise-mcp-server/
├── venv/                     # Virtual environment (created by Python)
├── mcp_server.py            # Main MCP server implementation ⭐
├── requirements.txt         # Python dependencies
├── test_mcp.py             # Testing script
├── vscode-settings.json    # VS Code configuration example
└── README.md               # Documentation
```

## Key Components Explained

### **1. MCP Server (`mcp_server.py`)**
- **Tool Definitions**: Each API endpoint becomes an MCP tool
- **Request Handler**: Converts MCP calls to HTTP requests
- **Response Formatter**: Makes API data conversational
- **Error Handling**: Graceful handling of failures

### **2. Tool Schema**
Each tool defines:
- **Name**: What the AI calls it (`get_profile`, `search_skills`)
- **Description**: When the AI should use it
- **Input Schema**: What parameters it accepts
- **Output Format**: How responses are structured

### **3. API Integration**
- **HTTP Client**: Async requests with proper timeouts
- **Authentication**: Headers and API keys (if needed)
- **Error Handling**: Network failures, API errors, rate limits

### **4. Response Formatting**
- **Human-Readable**: Convert JSON to conversational text
- **Structured Output**: Use markdown, emojis, formatting
- **Context Preservation**: Include relevant metadata

## How MCP Protocol Works

1. **Discovery**: AI assistant asks server "what tools do you have?"
2. **Tool Call**: AI decides to use a tool based on conversation
3. **Parameter Extraction**: AI provides required parameters
4. **API Request**: Server calls your API with parameters
5. **Response Formatting**: Server converts API response to text
6. **Natural Reply**: AI incorporates the data into conversation

## Next Steps

Now that you understand the architecture, let's build the actual MCP server in [Building the MCP Server](03-mcp-server.md).

---

**[← Previous: Prerequisites](01-prerequisites.md)** | **[Next: Building the MCP Server →](03-mcp-server.md)**