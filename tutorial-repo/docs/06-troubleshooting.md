# Comprehensive Troubleshooting Guide

This guide covers common issues when building and integrating MCP servers on Windows, with specific focus on the Luise API implementation.

## Quick Diagnostics Checklist

Before diving into specific issues, run through this checklist:

### Environment Verification

```powershell
# Check Python installation and version
python --version
# Should show: Python 3.11.x or 3.12.x

# Verify virtual environment activation
Get-Command python | Select-Object Source
# Should point to: ...\venv\Scripts\python.exe

# Check required packages
pip list | findstr -i "mcp httpx fastapi"

# Test API connectivity
curl https://api.m365princess.com/profile
# Should return JSON profile data

# Verify project structure
Get-ChildItem -Name
# Should show: mcp_server.py, requirements.txt, test_mcp.py
```

**All Green?** ✅ Skip to [Integration Issues](#integration-issues)  
**Any Red?** ❌ Continue reading the relevant section below

## Python Environment Issues

### Issue 1: Python Not Found

**Symptoms:**
```
'python' is not recognized as an internal or external command
```

**Solutions:**

**Option A: Install Python (Recommended)**
1. Visit [python.org](https://python.org/downloads/windows/)
2. Download Python 3.11 or 3.12
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. Restart PowerShell

**Option B: Use py Launcher**
```powershell
# Check if py launcher works
py --version

# If yes, use py instead of python throughout
py -m pip install --upgrade pip
py -m venv venv
```

**Option C: Microsoft Store Python**
```powershell
# Install via Windows Store (easier PATH management)
# Search "Python" in Microsoft Store
# Install "Python 3.11" or "Python 3.12"
```

### Issue 2: Wrong Python Version

**Check Version:**
```powershell
python --version
# If shows Python 2.x or very old 3.x
```

**Solutions:**

**Update Path Priority:**
```powershell
# Check all Python installations
where python
py -0  # List available versions

# Use specific version
py -3.11 -m venv venv
# or
py -3.12 -m venv venv
```

**Manual Path Edit:**
1. Windows + R → `sysdm.cpl` → Advanced → Environment Variables
2. Edit PATH: Move newer Python installation to top
3. Restart PowerShell

### Issue 3: Virtual Environment Problems

**Issue: venv creation fails**
```
Error: Unable to create process using 'c:\python\python.exe'
```

**Solution:**
```powershell
# Clear any existing venv folder
Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue

# Try different approaches
py -m venv venv                    # Method 1
python -m venv venv                # Method 2  
virtualenv venv                    # Method 3 (if installed)

# If all fail, use conda instead
conda create -n luise-mcp python=3.11
conda activate luise-mcp
```

**Issue: Virtual environment not activating**
```powershell
# Current symptom - still shows system Python
Get-Command python | Select-Object Source
# Shows: C:\Python311\python.exe instead of venv path
```

**Solution:**
```powershell
# Deactivate any existing environments
deactivate
conda deactivate  # if using conda

# Navigate to correct directory
cd C:\Users\$env:USERNAME\petprojects\luise-mcp-server

# Activate correctly (note the dot-sourcing)
. .\venv\Scripts\Activate.ps1

# Alternative syntax
venv\Scripts\Activate.ps1

# Verify activation worked
Get-Command python | Select-Object Source
# Should now show: ...\luise-mcp-server\venv\Scripts\python.exe
```

**Issue: Execution Policy prevents activation**
```
Execution policy error: cannot be loaded because running scripts is disabled
```

**Solution:**
```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy for current user (safe option)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Alternative: Run specific script
PowerShell.exe -ExecutionPolicy Bypass -File .\venv\Scripts\Activate.ps1
```

## Package Installation Issues

### Issue 4: pip Installation Failures

**General package errors:**
```
ERROR: Could not install packages due to an EnvironmentError
```

**Solutions:**

**Update pip first:**
```powershell
python -m pip install --upgrade pip setuptools wheel
```

**Try different installation methods:**
```powershell
# Method 1: Standard install
pip install -r requirements.txt

# Method 2: User install (if permissions issue)
pip install --user -r requirements.txt

# Method 3: No cache (if corrupted cache)
pip install --no-cache-dir -r requirements.txt

# Method 4: Verbose output to see what fails
pip install -r requirements.txt -v
```

**Specific package issues:**

**httpx SSL issues:**
```powershell
# Install with certificate verification workaround
pip install --trusted-host pypi.org --trusted-host pypi.python.org httpx
```

**MCP package not found:**
```powershell
# Ensure you're using correct package name
pip install mcp>=1.0.0

# If that fails, try development version
pip install git+https://github.com/modelcontextprotocol/python-sdk.git
```

### Issue 5: Dependency Conflicts

**Conflicting package versions:**
```
ERROR: pip's dependency resolver does not currently have a solution
```

**Solutions:**

**Check for conflicts:**
```powershell
pip check
```

**Clean installation:**
```powershell
# Remove and recreate venv
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install one by one to identify problematic package
pip install mcp
pip install httpx
pip install fastapi
pip install uvicorn
pip install pytest
```

**Use requirements without versions:**
```txt
mcp
httpx
fastapi
uvicorn
pytest
```

## MCP Server Issues

### Issue 6: Server Import Errors

**Common import failures:**

**MCP SDK import error:**
```python
ImportError: No module named 'mcp'
```

**Solution:**
```powershell
# Verify installation
pip show mcp

# Reinstall if necessary
pip uninstall mcp
pip install mcp>=1.0.0

# Check alternative names
pip install model-context-protocol
```

**httpx import error:**
```python
ImportError: No module named 'httpx'
```

**Solution:**
```powershell
pip install httpx>=0.25.0
```

### Issue 7: Server Runtime Errors

**API connection failures:**

**DNS resolution errors:**
```
httpx.ConnectError: [Errno -2] Name or service not known
```

**Check network connectivity:**
```powershell
# Test basic connectivity
Test-NetConnection api.m365princess.com -Port 443

# Test DNS resolution
nslookup api.m365princess.com

# Test with curl
curl -I https://api.m365princess.com/profile
```

**SSL Certificate errors:**
```
httpx.ConnectError: SSL: CERTIFICATE_VERIFY_FAILED
```

**Solutions:**
```python
# In mcp_server.py, modify the client creation:
client = httpx.AsyncClient(
    timeout=30.0,
    verify=False  # Only for testing - not recommended for production
)
```

**Better solution - update certificates:**
```powershell
# Update Windows certificates
certlm.msc  # Run and update if needed

# Alternative: Install certificates package
pip install certifi
```

**Timeout errors:**
```
httpx.TimeoutException: Request timed out
```

**Increase timeout in server:**
```python
client = httpx.AsyncClient(timeout=60.0)  # Increase from 30.0
```

### Issue 8: MCP Protocol Errors

**Tool registration issues:**
```
Error: Tool 'get_profile' not properly registered
```

**Check server initialization:**
```python
# Ensure @server.list_tools() decorator is present
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        # ... tool definitions
    ]
```

**Server startup failures:**
```
Error: Server failed to initialize
```

**Debug with basic server:**
```python
# Create minimal test server
import asyncio
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server

app = Server("test-server")

@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return []

if __name__ == "__main__":
    async def main():
        from mcp.server.stdio import stdio_server
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="test-server",
                    server_version="1.0.0",
                    capabilities=app.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

    asyncio.run(main())
```

## Testing Issues

### Issue 9: Test Script Failures

**test_mcp.py execution problems:**

**Script not found:**
```
python: can't open file 'test_mcp.py': [Errno 2] No such file or directory
```

**Verify file exists:**
```powershell
# Check current directory
Get-Location
ls

# If not in correct directory:
cd C:\Users\$env:USERNAME\petprojects\luise-mcp-server
```

**Import errors in tests:**
```python
ModuleNotFoundError: No module named 'test_imports'
```

**Solution - create the missing imports test:**
```python
# Add this at the top of test_mcp.py
import sys
import importlib.util

def test_imports():
    """Test that all required modules can be imported"""
    required_modules = ['mcp', 'httpx', 'asyncio', 'json', 'sys']
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            return False
    return True
```

**API connectivity test failures:**
```
❌ API Connectivity Test: Connection timeout
```

**Check network and firewall:**
```powershell
# Test Windows Firewall
netsh advfirewall show currentprofile

# Test corporate firewall/proxy
# Check with your IT team for proxy settings
```

### Issue 10: MCP Inspector Issues

**Inspector installation problems:**
```
npm: command not found
```

**Install Node.js:**
1. Visit [nodejs.org](https://nodejs.org)
2. Download and install LTS version  
3. Restart PowerShell
4. Verify: `node --version`

**Inspector execution errors:**
```
Error: Cannot resolve mcp_server.py
```

**Use full paths:**
```powershell
npx @modelcontextprotocol/inspector "C:\Users\$env:USERNAME\petprojects\luise-mcp-server\venv\Scripts\python.exe" "C:\Users\$env:USERNAME\petprojects\luise-mcp-server\mcp_server.py"
```

**Inspector connection timeouts:**
- Check that ports 3000+ are not blocked
- Try different port: `--port 3001`
- Check antivirus software - whitelist the inspector

## Integration Issues

### Issue 11: VS Code Configuration

**Settings.json syntax errors:**
```json
// Common mistake - trailing comma
{
  "mcp.servers": {
    "luise-api": {
      "command": "python",
      "args": ["C:\\Path\\To\\mcp_server.py"],  // Remove this comma
    }
  }
}
```

**Correct syntax:**
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
  }
}
```

**Path issues in VS Code:**
- Use double backslashes: `\\` 
- Or use forward slashes: `/`
- Avoid spaces in paths when possible

### Issue 12: GitHub Copilot Integration

**Copilot doesn't recognize MCP:**
1. **Update Extensions**: Ensure latest GitHub Copilot and MCP extensions
2. **Restart VS Code**: Full restart, not just reload window
3. **Check Extension Compatibility**: Some MCP extensions may conflict

**MCP commands not available:**
- Try different command prefixes: `@mcp`, `@tools`, `@context`
- Use Command Palette: `Ctrl+Shift+P` → "MCP"
- Check extension documentation for correct syntax

**Server connects but tools don't work:**
```powershell
# Test server independently
python mcp_server.py
# Should run without errors

# Check VS Code Output panel
# View → Output → Select "MCP" or "GitHub Copilot"
```

## Performance Issues

### Issue 13: Slow Response Times

**API responses are slow:**
- **Check internet speed**: Run speed test
- **Try different endpoints**: Test with `/profile` vs `/skills`
- **Increase timeouts** in mcp_server.py

**MCP server startup is slow:**
- **Reduce imports**: Only import what's needed
- **Check virtual environment**: Large venv can slow startup
- **Antivirus scanning**: Exclude Python/venv directory

### Issue 14: Memory Issues

**Python memory errors:**
```
MemoryError: Unable to allocate memory
```

**Solutions:**
- **Close other applications**
- **Restart VS Code**
- **Check Task Manager**: End unnecessary Python processes
- **Use 64-bit Python**: Ensure you're not using 32-bit version

## Development Workflow Issues

### Issue 15: Code Editing Problems

**VS Code Python extension issues:**
- **Install Python Extension**: Search "Python" in Extensions
- **Select Interpreter**: `Ctrl+Shift+P` → "Python: Select Interpreter"
- **Choose venv Python**: Select the one in `venv\Scripts\python.exe`

**IntelliSense not working:**
```json
// Add to VS Code settings.json
{
  "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
  "python.analysis.autoImportCompletions": true
}
```

### Issue 16: Git and Version Control

**Git not recognizing changes:**
```powershell
# Initialize git if needed
git init
git add .
git commit -m "Initial MCP server implementation"
```

**Large files in git:**
- Add `__pycache__/` to `.gitignore`
- Add `venv/` to `.gitignore`
- Add `.env` to `.gitignore`

## Error Code Reference

### HTTP Error Codes from API

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | Success | ✅ Working correctly |
| 404 | Not Found | Check endpoint spelling |
| 422 | Validation Error | Check query parameters |
| 429 | Rate Limited | Add delays between requests |
| 500 | Server Error | Try again later |
| 502/503 | Service Unavailable | API maintenance, try later |

### MCP Error Codes

| Error | Meaning | Solution |
|-------|---------|----------|
| `INVALID_REQUEST` | Malformed request | Check JSON formatting |
| `METHOD_NOT_FOUND` | Tool doesn't exist | Verify tool registration |
| `INVALID_PARAMS` | Wrong parameters | Check tool parameter schema |
| `INTERNAL_ERROR` | Server issue | Check server logs |

## Logs and Debugging

### Enable Debug Logging

**In mcp_server.py:**
```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**In VS Code:**
1. View → Output
2. Select dropdown → "MCP" or "GitHub Copilot"  
3. Look for error messages and stack traces

### Common Log Messages

**✅ Good logs:**
```
Making API request to: https://api.m365princess.com/profile
Response status: 200
Tool 'get_profile' executed successfully
```

**❌ Problem logs:**
```
Connection timeout after 30 seconds
HTTP 404: Endpoint not found
ImportError: No module named 'mcp'
```

## Getting Help

### Community Resources

1. **MCP GitHub**: [github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)
2. **GitHub Copilot Docs**: [docs.github.com/copilot](https://docs.github.com/copilot)
3. **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

### Creating Bug Reports

When asking for help, include:

```powershell
# System information
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
python --version
pip --version

# Package versions
pip list | findstr -i "mcp httpx fastapi"

# Error details
# Copy full error message and stack trace
```

### Test Script for Support

Create `debug_info.py`:
```python
import sys
import platform
import subprocess

print("=== Debug Information ===")
print(f"Python: {sys.version}")
print(f"Platform: {platform.platform()}")
print(f"Current directory: {os.getcwd()}")

# Test imports
for module in ['mcp', 'httpx', 'asyncio']:
    try:
        __import__(module)
        print(f"✅ {module} imported successfully")
    except ImportError as e:
        print(f"❌ {module} failed: {e}")

# Test API
import httpx
try:
    response = httpx.get("https://api.m365princess.com/profile", timeout=10)
    print(f"✅ API accessible: {response.status_code}")
except Exception as e:
    print(f"❌ API error: {e}")
```

Run with: `python debug_info.py`

## Recovery Procedures

### Complete Reset (Nuclear Option)

If everything is broken:

```powershell
# 1. Remove project directory
cd C:\Users\$env:USERNAME\petprojects
Remove-Item -Recurse -Force luise-mcp-server

# 2. Start fresh
mkdir luise-mcp-server
cd luise-mcp-server

# 3. Follow setup guide from Step 1
python -m venv venv
.\venv\Scripts\Activate.ps1
# ... continue with fresh installation
```

### Partial Reset (Selective Recovery)

**Reset Python environment only:**
```powershell
Remove-Item -Recurse -Force venv
python -m venv venv  
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Reset VS Code settings only:**
- Delete `.vscode/settings.json`
- Reconfigure MCP integration

**Reset MCP server only:**
- Download fresh `mcp_server.py` from tutorial
- Keep existing venv and requirements

---

This troubleshooting guide covers the most common issues when building MCP servers on Windows. Keep this guide handy as a reference when developing your own MCP integrations.

**Need more help?** Create an issue on the tutorial repository with your debug information and specific error messages.

---

**[← Previous: GitHub Copilot Integration](05-integration.md)** | **[Back to README →](../README.md)**