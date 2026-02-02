# Building the MCP Server

This is the core implementation section where we build the complete MCP server.

## Step 1: Create the Basic Server Structure

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

## Step 2: Define the API Helper Function

Add this function after the server initialization:

```python
async def make_api_request(endpoint: str, params: Optional[Dict[str, Any]] = None, 
                          method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Make an HTTP request to the Luise API."""
    url = f"{API_BASE_URL}{endpoint}"
    
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),  # 30 second timeout
        headers={"User-Agent": USER_AGENT}
    ) as client:
        try:
            logger.info(f"Making {method} request to {url} with params: {params}")
            
            if method == "GET":
                response = await client.get(url, params=params)
            elif method == "POST":
                response = await client.post(url, json=data, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
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

## Step 3: Define Your MCP Tools

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
        description="Submit a question to Luise (general Q&A, not talk-specific)",
        inputSchema={
            "type": "object",
            "properties": {
                "question": {
                    "type": "string", 
                    "description": "The question you want to ask"
                }
            },
            "required": ["question"]
        }
    )
]
```

**💡 Understanding Tools:**
- Each `Tool` maps to an API endpoint
- `inputSchema` defines what parameters the tool accepts
- AI assistants will see these descriptions and know when to use each tool

## Step 4: Implement Tool Registration

Add these two essential MCP server handlers:

```python
@mcp_server.list_tools()
async def list_tools() -> ListToolsResult:
    """List available tools - this tells AI clients what tools are available."""
    return ListToolsResult(tools=TOOLS)
```

**💡 What This Does:** When an AI assistant connects to your MCP server, it calls this function to discover what tools are available.

## Step 5: Implement the Core Tool Handler

This is the heart of your MCP server - the function that handles all tool calls. Due to length, I'll show the key pattern and a couple examples:

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
            profile_text = f"**{profile_data.get('name', 'Luise')}**\\n\\n"
            if 'title' in profile_data:
                profile_text += f"*{profile_data['title']}*\\n\\n"
            if 'bio' in profile_data:
                profile_text += f"{profile_data['bio']}\\n\\n"
            # ... more formatting
            
            return CallToolResult(content=[TextContent(type="text", text=profile_text)])
            
        elif name == "search_skills":
            # Handle skills search
            domain = arguments.get("domain")
            params = {"domain": domain} if domain else {}
            skills_data = await make_api_request("/skills", params)
            
            # Format skills response with emojis and structure
            skills_text = "🚀 **Technical Skills**"
            if domain:
                skills_text += f" (Domain: {domain})"
            skills_text += ":\\n\\n"
            
            for skill in skills_data['skills']:
                skills_text += f"**{skill.get('name', 'Unknown')}**"
                if 'level' in skill:
                    skills_text += f" - *{skill['level'].title()}*"
                # ... more formatting
            
            return CallToolResult(content=[TextContent(type="text", text=skills_text)])
            
        elif name == "get_quote":
            # Handle quote requests
            topic = arguments.get("topic", "general")
            params = {"topic": topic}
            quote_data = await make_api_request("/profile/quote", params)
            
            # Format quote response
            quote_text = f"💬 **Quote on {topic.title()}:**\\n\\n"
            quote_text += f"*\"{quote_data.get('quote', 'It depends on the context and requirements.')}\\"*\\n\\n"
            if 'author' in quote_data:
                quote_text += f"— {quote_data['author']}"
            
            return CallToolResult(content=[TextContent(type="text", text=quote_text)])
            
        elif name == "get_talks":
            # Handle talks requests
            year = arguments.get("year")
            params = {"year": year} if year else {}
            talks_data = await make_api_request("/talks", params)
            
            # Format talks response
            talks_text = "🎤 **Speaking Engagements"
            if year:
                talks_text += f" ({year})"
            talks_text += ":**\\n\\n"
            
            for talk in talks_data.get('talks', []):
                talks_text += f"**{talk.get('title', 'Untitled')}**\\n"
                if 'event' in talk:
                    talks_text += f"📍 {talk['event']}\\n"
                if 'date' in talk:
                    talks_text += f"📅 {talk['date']}\\n"
                if 'description' in talk:
                    talks_text += f"{talk['description']}\\n"
                talks_text += "\\n"
            
            return CallToolResult(content=[TextContent(type="text", text=talks_text)])
            
        elif name == "get_projects":
            # Handle projects requests
            projects_data = await make_api_request("/projects")
            
            # Format projects response
            projects_text = "🚀 **Projects & Portfolio:**\\n\\n"
            
            for project in projects_data.get('projects', []):
                projects_text += f"**{project.get('name', 'Unnamed Project')}**\\n"
                if 'description' in project:
                    projects_text += f"{project['description']}\\n"
                if 'technologies' in project:
                    tech_list = ', '.join(project['technologies'])
                    projects_text += f"🛠️ {tech_list}\\n"
                if 'status' in project:
                    projects_text += f"📊 Status: {project['status']}\\n"
                projects_text += "\\n"
            
            return CallToolResult(content=[TextContent(type="text", text=projects_text)])
            
        elif name == "submit_question":
            # Handle question submissions
            question = arguments.get("question", "")
            if not question:
                return CallToolResult(
                    content=[TextContent(type="text", text="❌ Error: Question cannot be empty")],
                    isError=True
                )
            
            # Post question to API
            post_data = {"question": question}
            response_data = await make_api_request("/questions", method="POST", data=post_data)
            
            # Format submission response
            response_text = f"✅ **Question Submitted Successfully!**\\n\\n"
            response_text += f"Your question: \\"{question}\\"\\n\\n"
            if 'id' in response_data:
                response_text += f"Question ID: {response_data['id']}\\n"
            response_text += "Thank you for your question! 💙"
            
            return CallToolResult(content=[TextContent(type="text", text=response_text)])
        
        else:
            # Handle unknown tools
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        # Handle any errors gracefully
        logger.error(f"Error in tool '{name}': {e}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"❌ Error executing {name}: {str(e)}")],
            isError=True
        )
```

## Step 6: Add the Main Function

Finally, add the entry point that starts the MCP server:

```python
async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server
    
    logger.info("Starting Luise API MCP Server...")
    logger.info(f"Server will connect to API at: {API_BASE_URL}")
    
    async with stdio_server() as (read_stream, write_stream):
## Step 6: Add Server Startup Code

Finally, add the code that starts your MCP server:

```python
async def main():
    """Main server entry point."""
    logger.info("Starting Luise API MCP Server...")
    logger.info(f"Server will connect to API at: {API_BASE_URL}")
    
    # Import needed for stdio server
    from mcp.server.stdio import stdio_server
    
    # Run server with stdin/stdout transport
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
- Starts the MCP server using stdio transport (standard input/output)
- This is the standard way MCP servers communicate with clients
- The server waits for MCP protocol messages from AI assistants

## Step 7: Test Your MCP Server

Open **PowerShell** in your project directory and test:

```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Test that your server starts without errors
python mcp_server.py
```

You should see output like:
```
2026-01-19 10:30:15 - __main__ - INFO - Starting Luise API MCP Server...
2026-01-19 10:30:15 - __main__ - INFO - Server will connect to API at: https://api.m365princess.com
```

**If it hangs without errors, that's good!** It means the server is waiting for MCP protocol messages. Press `Ctrl+C` to stop it.

## 📁 Complete Implementation

The complete `mcp_server.py` file is available in the [`src/`](../src/) directory of this repository. It includes:

- ✅ All 6 tool implementations
- ✅ Comprehensive error handling  
- ✅ Response formatting with emojis
- ✅ Support for both GET and POST requests
- ✅ Proper logging and debugging

## Next Steps

Now that your MCP server is built, let's test it thoroughly with the MCP Inspector in [Testing & Validation](04-testing.md).

---

**[← Previous: Project Setup](02-project-setup.md)** | **[Next: Testing & Validation →](04-testing.md)**