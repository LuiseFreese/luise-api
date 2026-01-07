#!/usr/bin/env python3

import asyncio
import json
from mcp_server import ProfileServer

async def test_mcp_tools():
    """Test our MCP server tools."""
    server = ProfileServer()
    
    print("=== Testing MCP Server Tools ===\n")
    
    # Test 1: Get Profile
    print("1. Testing get_profile...")
    try:
        result = await server.call_tool("get_profile", {})
        print(f"✅ get_profile: {json.dumps(result.content[0].text if result.content else 'No content', indent=2)[:200]}...")
    except Exception as e:
        print(f"❌ get_profile failed: {e}")
    
    # Test 2: Get Quote
    print("\n2. Testing get_quote...")
    try:
        result = await server.call_tool("get_quote", {"topic": "python"})
        print(f"✅ get_quote: {json.dumps(result.content[0].text if result.content else 'No content', indent=2)[:200]}...")
    except Exception as e:
        print(f"❌ get_quote failed: {e}")
    
    # Test 3: Search Skills
    print("\n3. Testing search_skills...")
    try:
        result = await server.call_tool("search_skills", {"domain": "development"})
        print(f"✅ search_skills: {json.dumps(result.content[0].text if result.content else 'No content', indent=2)[:200]}...")
    except Exception as e:
        print(f"❌ search_skills failed: {e}")
    
    # Test 4: Get Talks
    print("\n4. Testing get_talks...")
    try:
        result = await server.call_tool("get_talks", {})
        print(f"✅ get_talks: {json.dumps(result.content[0].text if result.content else 'No content', indent=2)[:200]}...")
    except Exception as e:
        print(f"❌ get_talks failed: {e}")
    
    # Test 5: Get Projects
    print("\n5. Testing get_projects...")
    try:
        result = await server.call_tool("get_projects", {})
        print(f"✅ get_projects: {json.dumps(result.content[0].text if result.content else 'No content', indent=2)[:200]}...")
    except Exception as e:
        print(f"❌ get_projects failed: {e}")
    
    # Test 6: Submit Question
    print("\n6. Testing submit_question...")
    try:
        result = await server.call_tool("submit_question", {
            "talk_id": "deploy-on-fridays-bonanni-2026",
            "name": "MCP Test User",
            "email": "test@mcp.example.com",
            "question": "This is a test question from the MCP server test script."
        })
        print(f"✅ submit_question: {json.dumps(result.content[0].text if result.content else 'No content', indent=2)[:200]}...")
    except Exception as e:
        print(f"❌ submit_question failed: {e}")
    
    print("\n=== MCP Server Test Complete ===")

if __name__ == "__main__":
    asyncio.run(test_mcp_tools())