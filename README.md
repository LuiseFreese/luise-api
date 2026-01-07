# Luise API

A playful REST API that serves as a personal introduction

## Features

- **Personal Profile API** - Get to know Luise
- **Skills & Expertise** - Technical skills with domain filtering and detailed information
- **Speaking History** - Past talks with detailed information
- **Project Portfolio** - Current and past open-source projects with architectural details

## Tech Stack

- **Python 3.11+** - Modern Python with type hints throughout
- **FastAPI** - High-performance async web framework
- **Pydantic v2** - Data validation and serialization
- **Uvicorn** - ASGI server for production-ready deployment
- **Pytest** - Comprehensive testing suite

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (or create the project structure):
   ```bash
   git clone https://github.com/example/luise-api.git
   cd luise-api
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Open your browser** and navigate to:
   - **API Documentation**: http://127.0.0.1:8000/docs
   - **Landing Page**: http://127.0.0.1:8000

## API Endpoints

### Profile Endpoints
- `GET /profile` - Get profile information

### Skills Endpoints
- `GET /skills` - List all skills with optional domain filtering

### Talks Endpoints
- `GET /talks` - List talks with optional year filtering
- `POST /talks/{talk_id}/questions` - Submit a question about a specific talk

### Projects Endpoints
- `GET /projects` - List all projects

### System Endpoints
- `GET /health` - Health check
- `GET /` - API documentation (Swagger UI)


## Example Usage

### Basic Profile Request
```bash
curl "http://127.0.0.1:8000/profile"
```

### Filter Skills by Domain
```bash
curl "http://127.0.0.1:8000/skills?domain=AI"
```

### Get Talks from Specific Year
```bash
curl "http://127.0.0.1:8000/talks?year=2025"
```

### Get All Projects
```bash
curl "http://127.0.0.1:8000/projects"
```

### Health Check
```bash
curl "http://127.0.0.1:8000/health"
```

### Submit Question for a Talk
```bash
curl -X POST "https://api.m365princess.com/talks/deploy-on-fridays-bonanni-2026/questions" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alex Developer",
    "email": "alex@example.com", 
    "question": "How do you handle CI/CD rollbacks when deployments fail on Fridays?"
  }'
```

### View Submitted Questions
You can view all submitted questions at:
- **Production**: https://api.m365princess.com/debug/file-contents

## Rate Limiting

The API includes rate limiting to prevent abuse and ensure fair usage:

### Rate Limits by Endpoint

- **Profile endpoints** (`/profile`): 60 requests/minute per IP
- **Skills/Talks/Projects endpoints**: 30 requests/minute per IP  
- **Question submission** (`POST /talks/{id}/questions`): **3 requests/minute per IP**
- **All other endpoints**: 30 requests/minute per IP

### Rate Limit Headers

When you make requests, you'll receive these headers:
- `X-RateLimit-Limit`: Total requests allowed in time window
- `X-RateLimit-Remaining`: Remaining requests in current window  
- `X-RateLimit-Reset`: UTC timestamp when limit resets

### Rate Limit Exceeded Response

When you exceed limits, you'll get a `429 Too Many Requests` response:
```json
{
  "error": "Rate limit exceeded: 3 per 1 minute"
}
```

## MCP Server

This repository includes an MCP (Model Context Protocol) server that exposes the API endpoints as AI tools.

### Quick MCP Setup

1. **Clone and install:**
```bash
git clone <your-repo-url>
cd luise-api
pip install -r requirements-mcp.txt
```

2. **Start the API server:**
```bash
python start.py
```

3. **Test MCP server:**
```bash
# In another terminal
python mcp_server.py
```

### Available MCP Tools

- `get_profile` - Get professional profile information
- `get_quote` - Get inspirational quotes on various topics  
- `search_skills` - Search skills by domain
- `get_talks` - Get conference talks and presentations
- `get_projects` - Get project information
- `submit_question` - Submit questions for talks

### VS Code Integration

Add to your VS Code `.vscode/mcp.json`:

```json
{
  "mcpServers": {
    "luise-profile": {
      "command": "python",
      "args": ["mcp_server.py"]
    }
  }
}
```

### Claude Desktop Integration

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "luise-profile": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"]
    }
  }
}
```

🚀 **That's it!** Share this repo and users can run your MCP server in under 2 minutes.

## VS Code Copilot Integration

Your MCP server is pre-configured to work with VS Code Copilot! The `.vscode/mcp.json` file automatically exposes your 6 MCP tools to Copilot.

### Quick Start

1. **Start both servers:**
   - Run task: `Run API Server` (Ctrl+Shift+P → Tasks: Run Task)
   - Run task: `Start MCP Inspector` (optional, for testing)

2. **Open Copilot Chat:**
   - Press `Ctrl+Shift+I` or click the Copilot chat icon

3. **Try these example prompts:**

```
@workspace What are Luise's AI and development skills?
```

```
@workspace Show me Luise's conference talks from 2026
```

```  
@workspace Get a motivational quote about Python development
```

```
@workspace What projects has Luise worked on recently?
```

```
@workspace Tell me about Luise's professional profile
```

### Advanced Copilot Queries

```
@workspace Use Luise's profile tools to help me write a speaker bio for her
```

```  
@workspace Based on Luise's skills, suggest what technologies she could mentor someone on
```

```
@workspace Compare Luise's 2026 talks and suggest follow-up topics
```

### Available Tools in Copilot

- **get_profile** - Professional profile information
- **get_quote** - Inspirational quotes by topic
- **search_skills** - Skills filtered by domain
- **get_talks** - Conference talks and presentations
- **get_projects** - Project information and details
- **submit_question** - Submit questions for talks

Copilot will automatically call these tools when relevant to answer your questions!
- **Local**: http://127.0.0.1:8000/debug/file-contents

## Running Tests

Run the test suite to ensure everything works correctly:

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage  
python -m pytest tests/ --cov=app

# Run specific test file
python -m pytest tests/test_api.py -v
```


## Architecture Highlights

### Clean Architecture Patterns
- **Separation of Concerns**: Models, services, and routers are cleanly separated
- **Dependency Injection**: Services are injected at the module level
- **Type Safety**: Comprehensive type hints throughout the codebase

### Error Handling
- **Consistent Error Format**: All errors follow the same JSON structure
- **Proper HTTP Status Codes**: Meaningful status codes for different scenarios
- **Detailed Error Messages**: Helpful error messages with context

### API Design
- **Read-Only**: Clean, safe GET-only endpoints
- **RESTful**: Follows REST conventions and best practices
- **Filtered Queries**: Support for domain/year filtering where appropriate

## Deployment

For production deployment, consider:

```bash
# Production server with Gunicorn
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Or using Uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Development Notes

### Code Style
- Type hints throughout the codebase
- Consistent naming conventions
- Comprehensive docstrings
- Clean separation between business logic and API routes

### Design Decisions
- **Read-Only API**: Clean GET-only methods for safe, simple demonstration
- **No Database**: Uses JSON files for easy setup and portability
- **Streamlined Endpoints**: Focused on essential functionality only
- **Error Handling**: Consistent error response format across all endpoints
- **Data Validation**: Leverages Pydantic v2 for comprehensive request/response validation
- **Modern Python**: Uses latest Pydantic patterns and type hints

## Contributing

This is a demo project, but if you'd like to suggest improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add or update tests
5. Submit a pull request
---

**Built with ❤️ **