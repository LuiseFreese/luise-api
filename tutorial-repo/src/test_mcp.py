#!/usr/bin/env python3
"""
Test suite for the Luise API MCP Server

Run this to verify your MCP server is working correctly.
Usage: python test_mcp.py
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
    
    try:
        # Try UTF-8 first, then fall back to other encodings
        content = ""
        for encoding in ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']:
            try:
                content = server_file.read_text(encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
        
        if not content:
            print_error("Could not read mcp_server.py with any encoding")
            return False
        
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
    
    except Exception as e:
        print_error(f"Error reading mcp_server.py: {e}")
        return False

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
        print("  2. Configure GitHub Copilot (see integration guide)")
        print("  3. Start chatting with AI assistants!")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ Some tests failed. Please fix the issues above.{Colors.END}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)