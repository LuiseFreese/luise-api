# Building Your First Model Context Protocol (MCP) Server: A Complete Guide

*Creating custom MCP servers to extend AI assistant capabilities with your own APIs and data sources*

## Table of Contents
1. [What is MCP and Why Should You Care?](#what-is-mcp-and-why-should-you-care)
2. [Prerequisites and Setup](#prerequisites-and-setup)
3. [Project Structure and Architecture](#project-structure-and-architecture)
4. [Building the MCP Server Step-by-Step](#building-the-mcp-server-step-by-step)
5. [Testing and Validation](#testing-and-validation)
6. [Deployment Options](#deployment-options)
7. [Integration with AI Clients](#integration-with-ai-clients)
8. [Best Practices and Troubleshooting](#best-practices-and-troubleshooting)

---

## What is MCP and Why Should You Care?

The **Model Context Protocol (MCP)** is an open standard that allows AI assistants like Claude Desktop, GitHub Copilot, and other MCP-compatible clients to securely connect to external data sources and services. Think of MCP servers as specialized connectors that expose your APIs, databases, or services as "tools" that AI assistants can use.

### Real-World Use Cases
- **Personal APIs**: Expose your portfolio, blog, or personal data to AI assistants
- **Company Data**: Connect internal systems, databases, or knowledge bases
- **Third-Party Services**: Integrate external APIs like GitHub, Slack, or custom services
- **Development Tools**: Create debugging helpers, code generators, or deployment assistants

### Our Real-World Example: The Luise API

In this tutorial, we'll build an MCP server that exposes the **Luise API** - a real FastAPI service that presents personal and professional information through a "REST meets self-introduction" API. 

**📝 Note:** While we use the Luise API as our example, you can easily adapt this tutorial to work with **any REST API** - your own personal API, company internal services, public APIs like GitHub or weather services, or any other HTTP-based data source. The patterns and code structure remain the same!

The Luise API includes endpoints for:

- **Profile information** with different modes (default, conference, afterhours)
- **Technical skills** searchable by domain
- **Speaking engagements** and talks
- **Project portfolio** and work samples
- **Interactive features** like quote generation and Q&A submission

By the end of this tutorial, you'll have built a complete MCP server that allows AI assistants to naturally query and interact with this personal API data.

---

## Prerequisites and Setup (Windows)

### System Requirements (Windows Only)
- **Windows 10 or 11** (64-bit)
- **Python 3.11 or 3.12** from [python.org](https://python.org/downloads)
- **PowerShell** or **Command Prompt**
- **Visual Studio Code** (recommended for development)
- **Basic understanding** of Python and APIs (we'll guide you through everything else!)

### Step 1: Install Python (If Not Already Installed)

1. **Download Python**: Visit [python.org/downloads](https://python.org/downloads) and download Python 3.12
2. **Run Installer**: 
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install for all users" (optional)
   - Click "Install Now"
3. **Verify Installation**: Open PowerShell and run:
   ```powershell
   python --version
   pip --version
   ```

### Step 2: Create Your Project Directory

Open **PowerShell** as Administrator and run:

```powershell
# Navigate to your development folder (adjust path as needed)
cd C:\Users\$env:USERNAME\petprojects

# Create project directory
mkdir luise-mcp-server
cd luise-mcp-server

# Create folder structure
mkdir app
mkdir tests
mkdir static
```

### Step 3: Set Up Python Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (IMPORTANT: You'll need to do this every time)
.\venv\Scripts\Activate.ps1

# Your prompt should now show (venv) at the beginning
# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 4: Install Required Packages

Create a `requirements.txt` file:
```powershell
# Create requirements file
New-Item -Path "requirements.txt" -ItemType File

# Add content to requirements.txt using PowerShell
@"
mcp>=1.0.0
httpx>=0.25.0
fastapi>=0.104.0
uvicorn>=0.24.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8
```

Install the packages:
```powershell
# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### Step 5: Install Node.js for MCP Inspector (Essential for Testing)

1. **Download Node.js**: Visit [nodejs.org](https://nodejs.org) and download the LTS version for Windows
2. **Run Installer**: Follow the installation wizard (keep all default settings)
3. **Verify Installation**: In PowerShell, run:
   ```powershell
   node --version
   npm --version
   ```
4. **Install MCP Inspector**:
   ```powershell
   npm install -g @modelcontextprotocol/inspector
   ```

---

## Project Structure and Architecture

Here's exactly what we'll build - a complete MCP server for the Luise API:

```
luise-mcp-server/
├── venv/                     # Virtual environment (created by Python)
├── mcp_server.py            # Main MCP server implementation ⭐
├── requirements.txt         # Python dependencies
├── test_mcp.py             # Testing script
├── claude-config.json      # Claude Desktop configuration
└── README.md               # Documentation
```

### Understanding the Luise API

The **Luise API** (hosted at `api.m365princess.com`) is a real FastAPI service with these endpoints:

- **`GET /profile`** - Personal profile with modes: `default`, `conference`, `afterhours`
  - Special unlock code: `unlock=ff69b4` reveals extra fields
- **`GET /profile/quote`** - Get quotes on various topics
- **`GET /skills`** - Technical skills (filterable by `domain`)
- **`GET /talks`** - Speaking engagements (filterable by `year`)
- **`GET /projects`** - Project portfolio 
- **`POST /talks/{id}/questions`** - Submit questions about talks

### MCP Server Architecture

```
[AI Assistant] ←→ [MCP Server] ←→ [Luise API]
     ↑               ↑               ↑
  Claude Desktop   mcp_server.py   api.m365princess.com
```

Each API endpoint becomes an **MCP Tool** that AI assistants can use naturally in conversation.

---

## Building the MCP Server Step-by-Step

### Step 1: Create the Basic Server Structure

Create a new file `mcp_server.py` in your project directory. In **VS Code** or **Notepad**, create this file with the following content:

```python
#!/usr/bin/env python3
"""
Luise API MCP Server

This MCP server exposes the Luise API endpoints as MCP tools, allowing AI clients
to interact with the personal introduction API through the Model Context Protocol.

Usage from PowerShell:
    python mcp_server.py
"""

import asyncio
import logging
import sys
from typing import Any, Dict, List, Optional

import httpx
from mcp.server import Server
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool

# Configure logging to stderr to avoid interfering with MCP protocol
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

# API configuration
API_BASE_URL = "https://api.m365princess.com"  # The real Luise API!
USER_AGENT = "luise-mcp-server/1.0.0"

# Initialize MCP server
mcp_server = Server("luise-api")
```

**💡 Important Notes:**
- We use `sys.stderr` for logging to avoid interfering with the MCP protocol
- The API_BASE_URL points to the real hosted Luise API
- We initialize the MCP server with the name "luise-api"

### Step 2: Define the API Helper Function

Add this function after the server initialization:

```python
async def make_api_request(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Make an HTTP request to the Luise API."""
    url = f"{API_BASE_URL}{endpoint}"
    
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),  # 30 second timeout
        headers={"User-Agent": USER_AGENT}
    ) as client:
        try:
            logger.info(f"Making API request to {url} with params: {params}")
            response = await client.get(url, params=params)
            response.raise_for_status()  # Raises exception for HTTP errors
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"API request failed: {e}")
            raise
```

**💡 What This Does:**
- Creates async HTTP client with proper timeout
- Handles errors gracefully
- Logs requests for debugging
- Returns JSON data from the API

### Step 3: Define Your MCP Tools

Add the tool definitions - these are the "functions" that AI assistants can use:

```python
# Tool definitions - each API endpoint becomes an MCP tool
TOOLS: List[Tool] = [
    Tool(
        name="get_profile",
        description="Get Luise's personal and professional profile information",
        inputSchema={
            "type": "object",
            "properties": {
                "mode": {
                    "type": "string",
                    "description": "Profile mode",
                    "enum": ["default", "conference", "afterhours"]
                },
                "unlock": {
                    "type": "string", 
                    "description": "Optional unlock code for additional profile fields"
                }
            }
        }
    ),
    Tool(
        name="get_quote",
        description="Get a quote from Luise on various topics",
        inputSchema={
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "Topic for the quote (e.g., 'technology', 'career', 'learning')"
                }
            }
        }
    ),
    Tool(
        name="search_skills",
        description="Search Luise's technical skills and expertise",
        inputSchema={
            "type": "object", 
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "Filter skills by domain (e.g., 'development', 'cloud', 'ai')"
                }
            }
        }
    ),
    Tool(
        name="get_talks",
        description="Get information about Luise's speaking engagements and presentations",
        inputSchema={
            "type": "object",
            "properties": {
                "year": {
                    "type": "integer",
                    "description": "Filter talks by year (e.g., 2024, 2023)"
                }
            }
        }
    ),
    Tool(
        name="get_projects",
        description="Get information about Luise's projects and work portfolio",
        inputSchema={
            "type": "object",
            "properties": {}  # No parameters needed for this endpoint
        }
    ),
    Tool(
        name="submit_question",
        description="Submit a question about one of Luise's talks",
        inputSchema={
            "type": "object",
            "properties": {
                "talk_id": {"type": "string", "description": "ID of the talk"},
                "name": {"type": "string", "description": "Your name"},
                "email": {"type": "string", "description": "Your email address"},
                "question": {"type": "string", "description": "Your question about the talk"}
            },
            "required": ["talk_id", "name", "email", "question"]
        }
    )
]
```

**💡 Understanding Tools:**
- Each `Tool` maps to an API endpoint
- `inputSchema` defines what parameters the tool accepts
- AI assistants will see these descriptions and know when to use each tool

### Step 4: Implement Tool Registration

Add these two essential MCP server handlers:

```python
@mcp_server.list_tools()
async def list_tools() -> ListToolsResult:
    """List available tools - this tells AI clients what tools are available."""
    return ListToolsResult(tools=TOOLS)
```

**💡 What This Does:** When an AI assistant connects to your MCP server, it calls this function to discover what tools are available.

### Step 5: Implement the Core Tool Handler

This is the heart of your MCP server - add this large function that handles all tool calls:

```python
@mcp_server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls - this is where the magic happens!"""
    try:
        if name == "get_profile":
            # Handle profile requests
            mode = arguments.get("mode", "default")
            unlock = arguments.get("unlock")
            params = {"mode": mode}
            if unlock:
                params["unlock"] = unlock
            
            profile_data = await make_api_request("/profile", params)
            
            # Format the response nicely for the AI
            profile_text = f"**{profile_data.get('name', 'Luise')}**\n\n"
            if 'title' in profile_data:
                profile_text += f"*{profile_data['title']}*\n\n"
            if 'bio' in profile_data:
                profile_text += f"{profile_data['bio']}\n\n"
            if 'location' in profile_data:
                profile_text += f"📍 **Location:** {profile_data['location']}\n"
            if 'email' in profile_data:
                profile_text += f"📧 **Email:** {profile_data['email']}\n"
            
            return CallToolResult(content=[TextContent(type="text", text=profile_text)])
            
        elif name == "get_quote":
            # Handle quote requests
            topic = arguments.get("topic")
            params = {"topic": topic} if topic else {}
            quote_data = await make_api_request("/profile/quote", params)
            
            quote_text = f"💭 **Quote"
            if topic:
                quote_text += f" on {topic}"
            quote_text += ":**\n\n"
            
            if 'quote' in quote_data:
                quote_text += f'"{quote_data["quote"]}"'
            if 'context' in quote_data:
                quote_text += f"\n\n*Context: {quote_data['context']}*"
            
            return CallToolResult(content=[TextContent(type="text", text=quote_text)])
            
        elif name == "search_skills":
            # Handle skills search
            domain = arguments.get("domain")
            params = {"domain": domain} if domain else {}
            skills_data = await make_api_request("/skills", params)
            
            if not skills_data or 'skills' not in skills_data:
                return CallToolResult(content=[TextContent(type="text", text="No skills data available.")])
                
            skills_text = "🚀 **Technical Skills**"
            if domain:
                skills_text += f" (Domain: {domain})"
            skills_text += ":\n\n"
            
            for skill in skills_data['skills']:
                skills_text += f"**{skill.get('name', 'Unknown')}**"
                if 'level' in skill:
                    skills_text += f" - *{skill['level'].title()}*"
                skills_text += "\n"
                if 'description' in skill:
                    skills_text += f"{skill['description']}\n"
                skills_text += "\n"
            
            return CallToolResult(content=[TextContent(type="text", text=skills_text)])
            
        elif name == "get_talks":
            # Handle talks requests
            year = arguments.get("year")
            params = {"year": year} if year else {}
            talks_data = await make_api_request("/talks", params)
            
            if not talks_data or 'talks' not in talks_data:
                return CallToolResult(content=[TextContent(type="text", text="No talks data available.")])
                
            talks_text = "🎤 **Speaking Engagements**"
            if year:
                talks_text += f" ({year})"
            talks_text += ":\n\n"
            
            if not talks_data['talks']:
                talks_text += f"⚠️ **No talks found for {year if year else 'any year'}.**\n"
                return CallToolResult(content=[TextContent(type="text", text=talks_text)])
            
            for talk in talks_data['talks']:
                talks_text += f"**{talk.get('title', 'Untitled Talk')}**\n"
                if 'event' in talk:
                    talks_text += f"📍 {talk['event']}"
                    if 'date' in talk:
                        talks_text += f" • {talk['date']}"
                    talks_text += "\n"
                if 'description' in talk:
                    talks_text += f"{talk['description']}\n"
                if 'id' in talk:
                    talks_text += f"*Use submit_question tool with talk_id: {talk['id']} to ask questions*\n"
                talks_text += "\n"
            
            return CallToolResult(content=[TextContent(type="text", text=talks_text)])
            
        elif name == "get_projects":
            # Handle projects requests
            projects_data = await make_api_request("/projects")
            
            if not projects_data or 'projects' not in projects_data:
                return CallToolResult(content=[TextContent(type="text", text="No projects data available.")])
                
            projects_text = "💻 **Project Portfolio:**\n\n"
            
            for project in projects_data['projects']:
                projects_text += f"**{project.get('name', 'Unnamed Project')}**\n"
                if 'description' in project:
                    projects_text += f"{project['description']}\n"
                if 'status' in project:
                    projects_text += f"Status: {project['status'].title()}\n"
                projects_text += "\n"
            
            return CallToolResult(content=[TextContent(type="text", text=projects_text)])
            
        elif name == "submit_question":
            # Handle question submission (POST request)
            talk_id = arguments.get("talk_id")
            name = arguments.get("name")
            email = arguments.get("email") 
            question = arguments.get("question")
            
            if not all([talk_id, name, email, question]):
                return CallToolResult(
                    content=[TextContent(type="text", text="Missing required parameters: talk_id, name, email, and question are all required.")],
                    isError=True
                )
            
            # Submit question via POST
            question_data = {"name": name, "email": email, "question": question}
            
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                headers={"User-Agent": USER_AGENT}
            ) as client:
                response = await client.post(
                    f"{API_BASE_URL}/talks/{talk_id}/questions",
                    json=question_data
                )
                response.raise_for_status()
                result = response.json()
            
            success_text = "✅ **Question submitted successfully!**\n\n"
            if 'question_id' in result:
                success_text += f"**Question ID:** {result['question_id']}\n"
            success_text += f"📋 **View questions:** {API_BASE_URL}/talks/{talk_id}/questions\n"
            
            return CallToolResult(content=[TextContent(type="text", text=success_text)])
            
        else:
            # Handle unknown tools
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        # Handle any errors gracefully
        logger.error(f"Error in tool '{name}': {e}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")],
            isError=True
        )
```

**💡 What This Giant Function Does:**
- Receives tool calls from AI assistants
- Routes to the correct API endpoint based on tool name
- Formats responses in human-readable format with emojis
- Handles errors gracefully
- Supports both GET and POST requests

### Step 6: Add the Main Function

Finally, add the entry point that starts the MCP server:

```python
async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server
    
    logger.info("Starting Luise API MCP Server...")
    logger.info(f"Server will connect to API at: {API_BASE_URL}")
    
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
```

**💡 What This Does:**
- Sets up stdio communication (standard input/output) for MCP protocol
- Starts the server and keeps it running
- Logs startup information

### Step 7: Test Your MCP Server

Open **PowerShell** in your project directory and test:

```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Test that your server starts without errors
python mcp_server.py
```

You should see output like:
```
2024-01-19 10:30:15 - __main__ - INFO - Starting Luise API MCP Server...
2024-01-19 10:30:15 - __main__ - INFO - Server will connect to API at: https://api.m365princess.com
```

**If it hangs without errors, that's good!** It means the server is waiting for MCP protocol messages. Press `Ctrl+C` to stop it.

---

## Testing and Validation

### Step 8: Advanced Testing with MCP Inspector

The **MCP Inspector** is your best friend for testing MCP servers. It provides a web interface to interact with your server exactly like an AI assistant would.

#### Start the MCP Inspector

Open **PowerShell** in your project directory:

```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Start the MCP Inspector with your server
npx @modelcontextprotocol/inspector python mcp_server.py
```

You should see output like:
```
MCP Inspector starting...
Server process started: python mcp_server.py
Inspector available at http://localhost:3000
```

#### Using the Web Interface

1. **Open Browser**: Go to `http://localhost:3000`
2. **See Your Tools**: You should see all 6 tools listed:
   - `get_profile`
   - `get_quote`  
   - `search_skills`
   - `get_talks`
   - `get_projects`
   - `submit_question`

3. **Test Each Tool**:

   **Test Profile (Basic)**:
   ```json
   {"mode": "default"}
   ```

   **Test Profile (With Easter Egg)**:
   ```json
   {"mode": "conference", "unlock": "ff69b4"}
   ```

   **Test Skills by Domain**:
   ```json
   {"domain": "development"}
   ```

   **Test Talks by Year**:
   ```json
   {"year": 2024}
   ```

   **Test Projects** (no parameters needed):
   ```json
   {}
   ```

4. **Check Results**: Each tool should return formatted, readable text with the actual data from the Luise API.

#### Troubleshooting Common Inspector Issues

**Problem**: "Failed to connect to server"
```powershell
# Check if Python is in PATH and virtual environment is active
python --version
# Should show Python 3.11+ and you should see (venv) in your prompt

# Try running the server directly first to check for errors
python mcp_server.py
```

**Problem**: "Module not found errors"
```powershell
# Reinstall dependencies
pip install --upgrade mcp httpx
```

**Problem**: "Server starts but tools don't work"
- Check the API is accessible: Visit `https://api.m365princess.com/profile` in your browser
- Look at the server logs in your PowerShell window for error messages

### Step 9: Create Automated Tests

Create a `test_mcp.py` file to validate your server automatically:

```python
#!/usr/bin/env python3
"""
Test script for the Luise API MCP Server

Run this to verify your MCP server is working correctly.
"""

import asyncio
import sys
import subprocess
import time
import httpx
import json
from pathlib import Path

class Colors:
    """ANSI color codes for pretty output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_test(message: str):
    """Print a test message"""
    print(f"{Colors.BLUE}[TEST]{Colors.END} {message}")

def print_success(message: str):
    """Print a success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message: str):
    """Print an error message"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message: str):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠️ {message}{Colors.END}")

async def test_api_connectivity():
    """Test that we can reach the Luise API directly"""
    print_test("Testing API connectivity...")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://api.m365princess.com/profile")
            if response.status_code == 200:
                data = response.json()
                if 'name' in data:
                    print_success(f"API is accessible - Found profile for: {data['name']}")
                    return True
                else:
                    print_warning("API responded but data format unexpected")
                    return False
            else:
                print_error(f"API responded with status {response.status_code}")
                return False
    except Exception as e:
        print_error(f"Cannot reach API: {e}")
        return False

def test_mcp_server_file():
    """Test that the MCP server file exists and has basic structure"""
    print_test("Checking MCP server file...")
    
    server_file = Path("mcp_server.py")
    if not server_file.exists():
        print_error("mcp_server.py file not found!")
        return False
    
    content = server_file.read_text()
    
    required_elements = [
        "from mcp.server import Server",
        "from mcp.types import",
        "API_BASE_URL",
        "mcp_server = Server",
        "@mcp_server.list_tools()",
        "@mcp_server.call_tool()",
        "async def main():"
    ]
    
    missing = []
    for element in required_elements:
        if element not in content:
            missing.append(element)
    
    if missing:
        print_error(f"Missing required elements: {', '.join(missing)}")
        return False
    
    print_success("MCP server file structure looks correct")
    return True

def test_python_imports():
    """Test that all required Python packages are installed"""
    print_test("Testing Python package imports...")
    
    try:
        import mcp
        import httpx
        import asyncio
        print_success("All required packages are installed")
        return True
    except ImportError as e:
        print_error(f"Missing required package: {e}")
        print_warning("Run: pip install -r requirements.txt")
        return False

async def test_mcp_server_startup():
    """Test that the MCP server can start without errors"""
    print_test("Testing MCP server startup...")
    
    try:
        # Start the server process
        process = subprocess.Popen(
            [sys.executable, "mcp_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give it a moment to start
        await asyncio.sleep(2)
        
        # Check if it's still running (no immediate crash)
        if process.poll() is None:
            print_success("MCP server starts successfully")
            process.terminate()
            process.wait()
            return True
        else:
            stdout, stderr = process.communicate()
            print_error("MCP server crashed on startup")
            if stderr:
                print_error(f"Error output: {stderr}")
            return False
            
    except Exception as e:
        print_error(f"Failed to start MCP server: {e}")
        return False

def test_requirements_file():
    """Test that requirements.txt exists and has necessary packages"""
    print_test("Checking requirements.txt...")
    
    req_file = Path("requirements.txt")
    if not req_file.exists():
        print_warning("requirements.txt not found")
        return False
    
    content = req_file.read_text().lower()
    required_packages = ["mcp", "httpx"]
    
    missing = []
    for package in required_packages:
        if package not in content:
            missing.append(package)
    
    if missing:
        print_warning(f"requirements.txt might be missing: {', '.join(missing)}")
        return False
    
    print_success("requirements.txt looks good")
    return True

async def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}🧪 Luise API MCP Server Test Suite{Colors.END}\n")
    
    tests = [
        ("Python Imports", test_python_imports),
        ("Requirements File", test_requirements_file),
        ("MCP Server File Structure", test_mcp_server_file),
        ("API Connectivity", test_api_connectivity),
        ("MCP Server Startup", test_mcp_server_startup),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{Colors.BOLD}Running: {test_name}{Colors.END}")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{Colors.BOLD}📊 Test Results Summary:{Colors.END}")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All tests passed! Your MCP server is ready to use.{Colors.END}")
        print(f"\n{Colors.BLUE}Next steps:{Colors.END}")
        print("  1. Test with MCP Inspector: npx @modelcontextprotocol/inspector python mcp_server.py")
        print("  2. Configure Claude Desktop (see blog post)")
        print("  3. Start chatting with AI assistants!")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ Some tests failed. Please fix the issues above.{Colors.END}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
```

#### Run the Tests

```powershell
# Make sure virtual environment is active
.\venv\Scripts\Activate.ps1

# Run the test suite
python test_mcp.py
```

You should see output like:
```
🧪 Luise API MCP Server Test Suite

Running: Python Imports
✅ All required packages are installed

Running: Requirements File  
✅ requirements.txt looks good

Running: MCP Server File Structure
✅ MCP server file structure looks correct

Running: API Connectivity
✅ API is accessible - Found profile for: Luise

Running: MCP Server Startup
✅ MCP server starts successfully

📊 Test Results Summary:
  ✅ PASS Python Imports
  ✅ PASS Requirements File
  ✅ PASS MCP Server File Structure
  ✅ PASS API Connectivity
  ✅ PASS MCP Server Startup

Results: 5/5 tests passed

🎉 All tests passed! Your MCP server is ready to use.
```

---

## Deployment Options

### Option 1: Local Development

For local development and testing:

```bash
# Run directly
python mcp_server.py

# Or with environment variables
LUISE_API_URL=http://localhost:8000 python mcp_server.py
```

### Option 2: Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy MCP server
COPY mcp_server.py .

# Create non-root user for security
RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser
USER mcpuser

# MCP servers typically use stdio transport
CMD ["python", "mcp_server.py"]
```

Build and run:

```bash
# Build container
docker build -t my-mcp-server .

# Run container (MCP servers typically don't need exposed ports for stdio transport)
docker run my-mcp-server
```

### Option 3: Cloud Deployment

For production deployment on cloud platforms:

**Railway/Render/Heroku:**
```bash
# Create Procfile
echo "mcp: python mcp_server.py" > Procfile
```

**systemd Service (Linux servers):**
```ini
[Unit]
Description=My MCP Server
After=network.target

[Service]
Type=simple
User=mcpuser
WorkingDirectory=/opt/my-mcp-server
Environment=PATH=/opt/my-mcp-server/venv/bin
ExecStart=/opt/my-mcp-server/venv/bin/python mcp_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## Integration with AI Clients (Windows)

Now for the exciting part - connecting your MCP server to AI assistants so you can chat with them about Luise's profile, skills, and projects!

### GitHub Copilot Configuration (Windows)

GitHub Copilot is an excellent MCP client through VS Code extensions. Here's how to set it up on Windows:

#### Step 10: Install Required Software

1. **Install VS Code**: Visit [code.visualstudio.com](https://code.visualstudio.com) if you don't have it
2. **Install GitHub Copilot**: 
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "GitHub Copilot" and install it
   - Sign in with your GitHub account

3. **Install MCP Extension for Copilot**:
   - Search for "MCP" or "Model Context Protocol" extensions
   - Install a compatible MCP client extension (e.g., "MCP Client" or similar)

#### Step 11: Configure VS Code for MCP

1. **Open VS Code Settings**:
   - Press `Ctrl+,` or go to File → Preferences → Settings
   - Click the "Open Settings (JSON)" icon in the top right

2. **Add MCP Configuration**:
   Add this to your `settings.json` file:

```json
{
  "mcp.servers": {
    "luise-api": {
      "command": "python",
      "args": ["C:\\Users\\YourUsername\\petprojects\\luise-mcp-server\\mcp_server.py"],
      "env": {
        "API_BASE_URL": "https://api.m365princess.com"
      }
    }
  },
  "github.copilot.enable": {
    "*": true,
    "plaintext": true,
    "markdown": true
  }
}
```

**⚠️ IMPORTANT:** Replace `YourUsername` with your actual Windows username and adjust the path to match where you created your project.

#### Step 12: Get Your Exact Path

To find the exact path, in **PowerShell** in your project directory:

```powershell
# Get the full path to your mcp_server.py file
Get-Location
# Copy this path and add \mcp_server.py to the end
```

Example paths:
- `C:\\Users\\john\\petprojects\\luise-mcp-server\\mcp_server.py`
- `C:\\Users\\sarah.smith\\petprojects\\luise-mcp-server\\mcp_server.py`

#### Step 13: Test the Integration

1. **Restart VS Code** completely (close and reopen)
2. **Open a New File**: Create a new file or open an existing project
3. **Check for MCP Integration**:
   - Open the Command Palette (`Ctrl+Shift+P`)
   - Type "MCP" to see if MCP commands are available
   - Look for any MCP status indicators in the status bar

4. **Test with GitHub Copilot Chat**:
   - Open Copilot Chat (`Ctrl+Shift+I` or click the chat icon)
   - Try these example prompts:

**Try these example prompts in Copilot Chat:**

```
@mcp Tell me about Luise's background and expertise
```

```
@mcp What technical skills does Luise have in the cloud domain?
```

```
@mcp Show me Luise's speaking engagements from 2024
```

```
@mcp Get Luise's profile in conference mode with the special unlock code ff69b4
```

```
@mcp What projects is Luise working on?
```

#### Alternative: Using MCP Tools Directly

If the extension supports direct tool access:

1. **Open Command Palette**: `Ctrl+Shift+P`
2. **Run MCP Tool**: Look for commands like "MCP: Execute Tool"
3. **Select Tool**: Choose from available tools (get_profile, search_skills, etc.)
4. **Provide Parameters**: Enter tool parameters as JSON

#### Troubleshooting GitHub Copilot Integration

**Problem: MCP commands don't appear in VS Code**

1. **Check Extension Installation**:
   ```powershell
   # In VS Code terminal
   code --list-extensions | findstr -i mcp
   ```

2. **Check Settings File**: Verify your `settings.json` is valid JSON
   - Go to Settings → Open Settings (JSON)
   - Look for syntax errors (red underlines)

3. **Check Python Path**: Make sure the path in settings.json is correct
   ```powershell
   # Test that the file exists
   Test-Path "C:\Users\YourUsername\petprojects\luise-mcp-server\mcp_server.py"
   ```

4. **Check VS Code Output**: 
   - Go to View → Output
   - Select "MCP" or "GitHub Copilot" from the dropdown
   - Look for error messages

**Problem: Copilot Chat doesn't recognize @mcp commands**

1. **Check MCP Extension Configuration**: The specific syntax depends on which MCP extension you're using
2. **Alternative Syntax**: Try different command formats:
   ```
   Use the Luise API MCP server to get profile information
   ```
   ```
   Call the get_profile tool with mode=conference
   ```

3. **Manual Tool Execution**: Use Command Palette → "MCP: Execute Tool"

**Problem: Tools connect but fail to execute**

1. **Test Your Server Separately**:
   ```powershell
   # Run the inspector to test your server
   npx @modelcontextprotocol/inspector python mcp_server.py
   ```

2. **Check Internet Connection**: The server needs to reach `api.m365princess.com`

3. **Check Virtual Environment**: Use full Python path in settings:

```json
{
  "mcp.servers": {
    "luise-api": {
      "command": "C:\\Users\\YourUsername\\petprojects\\luise-mcp-server\\venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\YourUsername\\petprojects\\luise-mcp-server\\mcp_server.py"],
      "env": {
        "API_BASE_URL": "https://api.m365princess.com"
      }
    }
  }
}
```

### Alternative Configuration for Different Environments

You can set up multiple configurations for different purposes in your VS Code settings:

```json
{
  "mcp.servers": {
    "luise-api-prod": {
      "command": "python",
      "args": ["C:\\Path\\To\\mcp_server.py"],
      "env": {
        "API_BASE_URL": "https://api.m365princess.com",
        "LOG_LEVEL": "INFO"
      }
    },
    "luise-api-debug": {
      "command": "python", 
      "args": ["C:\\Path\\To\\mcp_server.py"],
      "env": {
        "API_BASE_URL": "https://api.m365princess.com",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

### Other MCP-Compatible Clients (Windows)

While GitHub Copilot through VS Code is excellent for development, other options include:

#### Claude Desktop (Alternative Option)
- Download from [claude.ai/desktop](https://claude.ai/desktop)
- Configuration file: `%APPDATA%\Claude\claude_desktop_config.json`
- Similar JSON structure with `mcpServers` instead of `mcp.servers`

#### Zed Editor (Windows Available)
- Download from [zed.dev](https://zed.dev)
- Built-in MCP support with similar configuration

#### VS Code Extensions
Look for these extensions in the VS Code marketplace:
- **MCP Client** - Direct MCP protocol support
- **AI Assistant Extensions** - Various AI tools with MCP integration
- **GitHub Copilot Extensions** - Enhanced Copilot functionality

#### Custom Applications
Any application can implement MCP client functionality using the MCP SDK.

### Testing Your Integration

Once connected, test with these specific prompts in GitHub Copilot Chat:

1. **Profile Testing**:
   ```
   @mcp Show me Luise's profile in conference mode
   ```

2. **Skills Testing**:
   ```
   @mcp What are Luise's development skills?
   ```

3. **Talks Testing**:
   ```
   @mcp List Luise's talks from recent years
   ```

4. **Projects Testing**:
   ```
   @mcp Tell me about Luise's current projects
   ```

5. **Easter Egg Testing**:
   ```
   @mcp Get Luise's profile with the unlock code ff69b4
   ```

### Success Indicators

When everything is working correctly, you should see:

✅ **In VS Code**:
- MCP-related commands in Command Palette (`Ctrl+Shift+P`)
- MCP status indicators (depends on extension)
- No error messages in Output panels

✅ **In GitHub Copilot Chat**:
- `@mcp` commands are recognized
- AI responds with actual data from the Luise API
- Formatted responses with emojis and proper structure  
- Specific details about skills, talks, and projects

✅ **In Server Logs** (if running manually):
- "Making API request to..." messages
- HTTP 200 status codes  
- No error exceptions

### VS Code Workspace Integration

For better integration, you can also:

1. **Create a VS Code Workspace**: Save your MCP server project as a workspace
2. **Add Workspace Settings**: Include MCP configuration in `.vscode/settings.json`
3. **Create Tasks**: Add VS Code tasks to start/stop your MCP server
4. **Use Integrated Terminal**: Run MCP Inspector directly from VS Code terminal

---

## Best Practices and Troubleshooting (Windows)

### Windows-Specific Best Practices

#### File Paths and Backslashes
Windows uses backslashes in paths, which need special handling in JSON:

**✅ Correct JSON Configuration:**
```json
{
  "mcpServers": {
    "luise-api": {
      "command": "python",
      "args": ["C:\\Users\\username\\petprojects\\luise-mcp-server\\mcp_server.py"]
    }
  }
}
```

**❌ Common Mistake:**
```json
{
  "args": ["C:\Users\username\petprojects\luise-mcp-server\mcp_server.py"]
}
```

#### PowerShell vs Command Prompt
Use **PowerShell** instead of Command Prompt for better Unicode support and modern features:

```powershell
# Good: Use PowerShell
cd "C:\Users\$env:USERNAME\petprojects\luise-mcp-server"
.\venv\Scripts\Activate.ps1

# Avoid: Old Command Prompt
# cmd.exe has encoding issues and limited features
```

#### Virtual Environment Best Practices

**Option 1: Use Full Python Path in Configuration**
```json
{
  "command": "C:\\Users\\username\\petprojects\\luise-mcp-server\\venv\\Scripts\\python.exe",
  "args": ["C:\\Users\\username\\petprojects\\luise-mcp-server\\mcp_server.py"]
}
```

**Option 2: Install Packages Globally (Not Recommended)**
```powershell
# Only if you can't get virtual environments working with Claude
pip install mcp httpx
```

### Security Best Practices

#### 1. Input Validation for Windows Paths
```python
import os
from pathlib import Path

def validate_windows_path(path_str: str) -> bool:
    """Validate Windows file paths safely."""
    try:
        path = Path(path_str)
        # Check for directory traversal attempts
        if ".." in path.parts:
            return False
        # Ensure path is within expected directory
        if not path.is_absolute():
            return False
        return True
    except Exception:
        return False
```

#### 2. Environment Variables for Sensitive Data
```python
import os

# Use environment variables for API keys or sensitive URLs
API_KEY = os.getenv("LUISE_API_KEY")  # Set in Windows Environment Variables
API_BASE_URL = os.getenv("LUISE_API_URL", "https://api.m365princess.com")  # Default fallback
```

**Set Environment Variables in Windows:**
```powershell
# Temporarily (current session only)
$env:LUISE_API_KEY = "your-api-key-here"

# Permanently (requires restart)
[Environment]::SetEnvironmentVariable("LUISE_API_KEY", "your-api-key", "User")
```

#### 3. Error Handling for Windows-Specific Issues
```python
import sys
import traceback

async def make_api_request(endpoint: str) -> Dict[str, Any]:
    """Windows-safe API request with proper error handling."""
    try:
        # Your existing request logic
        pass
    except httpx.ConnectTimeout:
        logger.error("Network timeout - check your internet connection")
        raise
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            logger.error("API access forbidden - check your API key")
        raise
    except Exception as e:
        # Log the full traceback on Windows for debugging
        logger.error(f"Unexpected error: {e}")
        logger.debug(traceback.format_exc())
        raise
```

### Performance Optimization (Windows)

#### 1. Windows Defender Exclusions
Add your project folder to Windows Defender exclusions to improve performance:

1. **Open Windows Security**: Search "Windows Security" in Start Menu
2. **Virus & Threat Protection** → **Manage Settings** under "Virus & threat protection settings"
3. **Add or Remove Exclusions** → **Add an exclusion** → **Folder**
4. **Select your project folder**: `C:\Users\username\petprojects\luise-mcp-server`

#### 2. PowerShell Execution Policy
Set appropriate execution policy for running scripts:

```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy for current user (recommended)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# More restrictive (only signed scripts)
Set-ExecutionPolicy -ExecutionPolicy AllSigned -Scope CurrentUser
```

#### 3. Connection Pooling and Timeouts
```python
# Optimize for Windows network stack
http_client = httpx.AsyncClient(
    timeout=httpx.Timeout(
        connect=10.0,  # Connection timeout
        read=30.0,     # Read timeout
        write=5.0,     # Write timeout
        pool=30.0      # Pool timeout
    ),
    limits=httpx.Limits(
        max_keepalive_connections=5,
        max_connections=10,
        keepalive_expiry=30.0
    )
)
```

### Common Windows Issues and Solutions

#### Issue 1: "Python is not recognized as an internal or external command"

**Solution**:
```powershell
# Check if Python is in PATH
$env:PATH -split ';' | Where-Object { $_ -like '*Python*' }

# If not found, add Python to PATH manually:
# 1. Find Python installation
Get-Command python -ErrorAction SilentlyContinue

# 2. Add to PATH if needed (replace with your Python path)
$env:PATH += ";C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python311\Scripts"
$env:PATH += ";C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python311"
```

**Permanent Solution**:
1. **System Properties** → **Environment Variables**
2. **Edit PATH** → **Add Python paths**
3. **Restart PowerShell**

#### Issue 2: "Execution policy errors when activating virtual environment"

**Solution**:
```powershell
# Option 1: Change execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Option 2: Bypass for single command
PowerShell.exe -ExecutionPolicy Bypass -File ".\venv\Scripts\Activate.ps1"

# Option 3: Use activation batch file instead
.\venv\Scripts\activate.bat
```

#### Issue 3: "Module not found" errors with virtual environment

**Solution**:
```powershell
# Verify virtual environment is active (you should see (venv) in prompt)
# If not:
.\venv\Scripts\Activate.ps1

# Verify packages are installed in virtual environment
pip list

# If packages missing, reinstall:
pip install -r requirements.txt

# Check which Python pip is using:
pip --version
```

#### Issue 4: "Access denied" or permission errors

**Solution**:
```powershell
# Run PowerShell as Administrator for installation issues
# For project work, use regular user permissions

# Check file permissions:
Get-Acl "mcp_server.py" | Format-List

# Fix permissions if needed:
icacls "mcp_server.py" /grant "$env:USERNAME:(F)"
```

#### Issue 5: "Unicode/encoding errors" in Windows console

**Solution**:
```powershell
# Set UTF-8 encoding for current session
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001

# Or use Windows Terminal instead of old console
```

**In your Python code:**
```python
import sys
import locale

# Ensure proper encoding on Windows
if sys.platform == "win32":
    # Set UTF-8 encoding for stdout/stderr
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
```

#### Issue 6: "GitHub Copilot doesn't recognize MCP commands"

**Diagnostic Steps**:
```powershell
# 1. Check VS Code settings file
Get-Content "$env:APPDATA\Code\User\settings.json" | ConvertFrom-Json

# 2. Verify MCP extension is installed
code --list-extensions | findstr -i mcp

# 3. Test server manually
python mcp_server.py

# 4. Check Python path in settings matches reality
(Get-Command python).Source
```

#### Issue 7: "VS Code MCP integration not working"

**Solutions**:
```powershell
# 1. Restart VS Code completely
# 2. Check VS Code Output panels for errors
# View -> Output -> Select "MCP" or "GitHub Copilot"

# 3. Try alternative MCP extensions
# Extensions -> Search "Model Context Protocol"

# 4. Use full Python executable path in settings.json:
```

```json
{
  "mcp.servers": {
    "luise-api": {
      "command": "C:\\Users\\YourUsername\\AppData\\Local\\Programs\\Python\\Python312\\python.exe",
      "args": ["C:\\Full\\Path\\To\\mcp_server.py"]
    }
  }
}
```

### Debugging Tips (Windows)

#### 1. Enhanced Logging
```python
import logging
import sys
from pathlib import Path

# Create logs directory
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Set up file and console logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # Console output (stderr for MCP compatibility)
        logging.StreamHandler(sys.stderr),
        # File output for debugging
        logging.FileHandler(log_dir / "mcp_server.log")
    ]
)
```

#### 2. Windows Event Logging (Advanced)
```python
import logging.handlers

# Log to Windows Event Log (requires pywin32)
try:
    handler = logging.handlers.NTEventLogHandler("Luise MCP Server")
    handler.setLevel(logging.ERROR)
    logging.getLogger().addHandler(handler)
except ImportError:
    pass  # Skip if pywin32 not available
```

#### 3. Performance Monitoring
```python
import time
import psutil
import os

def log_system_info():
    """Log system information for debugging."""
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    cpu_percent = process.cpu_percent()
    
    logger.info(f"System: Memory={memory_mb:.1f}MB, CPU={cpu_percent:.1f}%")

# Call periodically in your server
async def periodic_monitoring():
    while True:
        log_system_info()
        await asyncio.sleep(60)  # Log every minute
```

### Deployment Recommendations (Windows)

#### For Production Use:
1. **Windows Service**: Convert your MCP server to a Windows service using `pywin32`
2. **Task Scheduler**: Use Windows Task Scheduler for automated startup
3. **IIS Integration**: Use IIS with FastCGI for web-accessible endpoints
4. **Docker**: Use Windows containers for consistent deployment

#### For Development:
1. **VS Code Integration**: Use VS Code with Python extensions
2. **Windows Terminal**: Better console experience than Command Prompt
3. **Git for Windows**: Proper version control with Windows line endings
4. **Windows Subsystem for Linux**: Alternative environment if needed

---

## Conclusion

Congratulations! 🎉 You've just built a complete, production-ready MCP server that connects the real Luise API to AI assistants. This is no toy project - you've created something that demonstrates the true power of the Model Context Protocol.

### What You've Accomplished

✅ **Built a Real MCP Server**: Your server exposes 6 different tools that AI assistants can use naturally  
✅ **Connected to a Live API**: You're pulling real data from `api.m365princess.com`  
✅ **Implemented Proper Error Handling**: Your server gracefully handles network issues and API errors  
✅ **Added Comprehensive Testing**: Both automated tests and interactive testing with MCP Inspector  
✅ **Configured AI Assistant Integration**: Claude Desktop can now access the Luise API through your server  
✅ **Applied Windows Best Practices**: Virtual environments, proper file paths, and PowerShell usage  

### The Magic You've Created

With your MCP server running, AI assistants can now:

- **Naturally ask about Luise's background**: "Tell me about Luise's technical expertise"
- **Search skills by domain**: "What cloud skills does Luise have?"
- **Browse speaking history**: "Show me Luise's talks from recent years"  
- **Explore project portfolio**: "What projects is Luise working on?"
- **Access Easter eggs**: "Get Luise's profile with the unlock code"
- **Submit questions about talks**: "I want to ask a question about one of her presentations"

All of this happens seamlessly in natural conversation - the AI assistant knows when to call your MCP tools and formats the responses beautifully.

### Key Concepts You've Mastered

🧠 **MCP Protocol Understanding**: You now understand how AI assistants discover and use external tools  
🔧 **Tool Design**: Each API endpoint becomes a focused, well-documented tool  
🌐 **Async API Integration**: Proper HTTP client usage with timeouts and error handling  
📝 **Response Formatting**: Converting API data into human-readable, conversational content  
🔍 **Testing Strategies**: Both automated testing and interactive debugging approaches  
🖥️ **Windows Development**: Virtual environments, PowerShell, and Windows-specific configurations  

### Real-World Applications

Now that you understand the pattern, you can build MCP servers for:

#### Personal Use Cases
- **Your own portfolio API** - Expose your resume, projects, and skills
- **Personal note-taking systems** - Connect Notion, Obsidian, or custom databases  
- **Home automation** - Control IoT devices through AI conversation
- **Financial tracking** - Query your expense tracking or investment APIs

#### Professional Use Cases  
- **Company knowledge bases** - Connect internal wikis, documentation, or databases
- **CRM integration** - Allow AI assistants to query customer data
- **Development tools** - Expose CI/CD status, deployment info, or monitoring data
- **Support systems** - Connect ticketing systems or FAQ databases

#### Community Projects
- **Public APIs** - Weather, news, sports scores, or social media data
- **Educational content** - Course materials, tutorials, or reference data
- **Open data** - Government APIs, scientific databases, or public datasets

### Next Steps: Taking It Further

#### 1. Enhance Your Current Server
```python
# Add authentication
async def authenticate_request(api_key: str) -> bool:
    # Implement API key validation
    pass

# Add caching for better performance  
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_profile(mode: str) -> dict:
    # Cache frequently requested data
    pass

# Add more sophisticated error handling
async def retry_with_backoff(func, max_retries=3):
    # Implement exponential backoff
    pass
```

#### 2. Create Your Own API
Build a FastAPI service (like the Luise API) that serves your own data:
```python
from fastapi import FastAPI

app = FastAPI(title="My Personal API")

@app.get("/profile")
async def get_my_profile():
    return {"name": "Your Name", "bio": "Your Bio"}
```

#### 3. Advanced MCP Features
- **File operations**: Let AI assistants read/write files through MCP
- **Database connections**: Direct database queries through MCP tools
- **Real-time data**: WebSocket connections for live data feeds
- **Batch operations**: Process multiple requests efficiently

#### 4. Deploy to Production
- **Cloud deployment**: Railway, Render, or Azure Container Instances
- **Monitoring**: Add health checks and metrics
- **Security**: API rate limiting and authentication
- **High availability**: Multiple instances and load balancing

### Join the MCP Community

The Model Context Protocol ecosystem is rapidly growing:

🌟 **Share Your Server**: Consider open-sourcing your MCP server on GitHub  
📚 **Contribute Documentation**: Help others learn by writing tutorials  
💡 **Build Creative Integrations**: Connect unexpected APIs and services  
🤝 **Collaborate**: Join MCP discussions and help solve common challenges  

### Resources for Continued Learning

- **MCP Specification**: [spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io)
- **Official Python SDK**: [GitHub - MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- **MCP Inspector**: [GitHub - MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- **Community Examples**: [GitHub - MCP Servers](https://github.com/modelcontextprotocol/servers)
- **Claude Desktop**: [claude.ai/desktop](https://claude.ai/desktop)

### Final Thoughts

You've just built something that bridges the gap between AI assistants and real-world data. Every time you chat with Claude Desktop about Luise's skills or projects, remember that it's YOUR MCP server making that conversation possible.

This is just the beginning. The future of AI assistants depends on developers like you building the connectors that make AI truly useful in real-world scenarios. Whether it's helping someone learn about a professional's background, accessing company data, or automating daily tasks - MCP servers are the key that unlocks AI's potential.

**Now go build something amazing!** 🚀

---

### Quick Reference Card

**Start Your Server:**
```powershell
.\venv\Scripts\Activate.ps1
python mcp_server.py
```

**Test with Inspector:**
```powershell
npx @modelcontextprotocol/inspector python mcp_server.py
```

**VS Code Settings Location:**
```
%APPDATA%\Code\User\settings.json
```

**GitHub Copilot Chat Commands:**
- `@mcp Tell me about Luise's background`
- `@mcp What are her cloud skills?`  
- `@mcp Show me talks from 2024`
- `@mcp Get profile with unlock code ff69b4`

**Alternative Commands (if @mcp doesn't work):**
- "Use the Luise API to get profile information"
- "Call the MCP server to search for development skills"

---

*Happy building! The MCP ecosystem grows stronger with every server you create. Share your creations and help expand what's possible when AI assistants can connect to the real world.*