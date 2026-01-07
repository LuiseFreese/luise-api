#!/usr/bin/env python3
"""
Luise API MCP Server

This MCP server exposes the Luise API endpoints as MCP tools, allowing AI clients
to interact with the personal introduction API through the Model Context Protocol.

Usage:
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
API_BASE_URL = "https://api.m365princess.com"
USER_AGENT = "luise-mcp-server/1.0.0"

# Initialize MCP server
mcp_server = Server("luise-api")


async def make_api_request(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Make an HTTP request to the Luise API."""
    url = f"{API_BASE_URL}{endpoint}"
    
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
        headers={"User-Agent": USER_AGENT}
    ) as client:
        try:
            logger.info(f"Making API request to {url} with params: {params}")
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"API request failed: {e}")
            raise


# Tool definitions
TOOLS: List[Tool] = [
    Tool(
        name="get_profile",
        description="Get ONLY Luise's actual profile data from her API. Returns exact database content - do not add external information.",
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
                    "description": "Topic for the quote"
                }
            }
        }
    ),
    Tool(
        name="search_skills",
        description="Search ONLY the skills listed in Luise's database. Returns exact skill data without additions.",
        inputSchema={
            "type": "object", 
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "Filter skills by domain"
                }
            }
        }
    ),
    Tool(
        name="get_talks",
        description="Get ONLY the speaking engagements that exist in Luise's database. Returns actual talk data only - do not add, invent, or assume additional talks.",
        inputSchema={
            "type": "object",
            "properties": {
                "year": {
                    "type": "integer",
                    "description": "Filter talks by year"
                }
            }
        }
    ),
    Tool(
        name="get_projects",
        description="Get information about Luise's projects",
        inputSchema={
            "type": "object",
            "properties": {}
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
                "question": {"type": "string", "description": "Your question"}
            },
            "required": ["talk_id", "name", "email", "question"]
        }
    )
]


@mcp_server.list_tools()
async def list_tools() -> ListToolsResult:
    """List available tools."""
    return ListToolsResult(tools=TOOLS)


@mcp_server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    try:
        if name == "get_profile":
            mode = arguments.get("mode", "default")
            unlock = arguments.get("unlock")
            params = {"mode": mode}
            if unlock:
                params["unlock"] = unlock
            
            profile_data = await make_api_request("/profile", params)
            
            # Format the response
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
            year = arguments.get("year")
            params = {"year": year} if year else {}
            talks_data = await make_api_request("/talks", params)
            
            if not talks_data or 'talks' not in talks_data:
                return CallToolResult(content=[TextContent(type="text", text="No talks data available.")])
                
            talks_text = "🎤 **Speaking Engagements FROM LUISE'S API DATABASE**"
            if year:
                talks_text += f" ({year})"
            talks_text += ":\n\n"
            
            if not talks_data['talks']:
                talks_text += f"⚠️ **No talks found in database for {year if year else 'any year'}.**\n"
                talks_text += "**This data comes directly from the API - no additional talks exist.**\n"
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
            
            talks_text += "\n---\n**📊 Data Source:** Live API at api.m365princess.com\n**Total Results:** " + str(len(talks_data['talks'])) + " talk(s)\n"
            
            return CallToolResult(content=[TextContent(type="text", text=talks_text)])
            
        elif name == "get_projects":
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
            talk_id = arguments.get("talk_id")
            name = arguments.get("name")
            email = arguments.get("email") 
            question = arguments.get("question")
            
            if not all([talk_id, name, email, question]):
                return CallToolResult(
                    content=[TextContent(type="text", text="Missing required parameters.")],
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
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Error in tool '{name}': {e}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")],
            isError=True
        )


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