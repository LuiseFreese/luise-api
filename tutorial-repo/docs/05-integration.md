# GitHub Copilot Integration (Windows)

This guide covers connecting your MCP server to GitHub Copilot in VS Code on Windows.

## Prerequisites

Before starting, ensure you have:
- ✅ Completed all previous setup steps
- ✅ MCP server passing all tests
- ✅ VS Code installed
- ✅ GitHub Copilot subscription and extension installed

## Step 10: Install Required Software

### VS Code and Extensions

1. **Install VS Code**: Visit [code.visualstudio.com](https://code.visualstudio.com) if you don't have it
2. **Install GitHub Copilot**: 
   - Open VS Code
   - Go to Extensions
   - Search for "GitHub Copilot" and install it
   - Sign in with your GitHub account

3. **Install MCP Extension**:
   - Search for "MCP" or "Model Context Protocol" extensions
   - Install a compatible MCP client extension (e.g., "MCP Client" or similar)
   - Note: MCP extension ecosystem is growing, check for latest options

## Step 11: Configure VS Code for MCP

### Method 1: User Settings (Recommended)

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

**⚠️ IMPORTANT:** Replace `YourUsername` with your actual Windows username.

### Method 2: Workspace Settings (Project-Specific)

1. **Create Workspace Settings**:
   In your project root, create `.vscode/settings.json`:

```json
{
  "mcp.servers": {
    "luise-api": {
      "command": "python",
      "args": ["${workspaceFolder}/mcp_server.py"],
      "env": {
        "API_BASE_URL": "https://api.m365princess.com"
      }
    }
  }
}
```

This approach uses relative paths and is better for sharing projects.

## Step 12: Get Your Exact Path

To find the exact path for your configuration:

```powershell
# Navigate to your project directory
cd C:\Users\$env:USERNAME\petprojects\luise-mcp-server

# Get the full path to your mcp_server.py file
Get-Location
# Copy this path and add \mcp_server.py to the end
```

**Example paths:**
- `C:\\Users\\john\\petprojects\\luise-mcp-server\\mcp_server.py`
- `C:\\Users\\sarah.smith\\petprojects\\luise-mcp-server\\mcp_server.py`

**Note the double backslashes** in JSON - this is required for Windows paths.

## Step 13: Test the Integration

### 1. Restart VS Code
- Close VS Code completely
- Reopen VS Code and open your project folder

### 2. Check MCP Status
- Open the Command Palette (`Ctrl+Shift+P`)
- Type "MCP" to see if MCP commands are available
- Look for any MCP status indicators in the status bar

### 3. Test with GitHub Copilot Chat

Open Copilot Chat (`Ctrl+Shift+I` or click the chat icon) and try these examples:

**Basic Profile Query:**
```
@mcp Tell me about Luise's background and expertise
```

**Skills Search:**
```
@mcp What technical skills does Luise have in the cloud domain?
```

**Speaking History:**
```
@mcp Show me Luise's speaking engagements from 2024
```

**Easter Egg Test:**
```
@mcp Get Luise's profile in conference mode with the unlock code ff69b4
```

**Project Information:**
```
@mcp What projects is Luise working on?
```

### Expected Results

**✅ Successful Integration:**
You should see responses like:
```
🚀 **Technical Skills (Domain: cloud):**

**Azure** - *Expert*
Microsoft Azure cloud platform with extensive experience in container orchestration, serverless computing...

**AWS** - *Advanced*  
Amazon Web Services for scalable cloud solutions, including Lambda, ECS, and machine learning pipelines...
```

## Alternative Command Syntax

If `@mcp` commands don't work, try these alternatives:

**Natural Language:**
```
Use the Luise API MCP server to get profile information
```

**Direct Tool Reference:**
```
Call the get_profile tool with mode=conference
```

**Manual Tool Execution:**
- Command Palette (`Ctrl+Shift+P`) 
- "MCP: Execute Tool"
- Select tool and provide parameters

## Troubleshooting Integration Issues

### Issue 1: MCP commands don't appear in VS Code

**Check Extension Installation:**
```powershell
# List installed extensions
code --list-extensions | findstr -i mcp
```

**Verify Settings:**
1. Go to Settings → Open Settings (JSON)
2. Look for syntax errors (red underlines)
3. Validate JSON at [jsonlint.com](https://jsonlint.com)

**Check VS Code Output:**
1. View → Output
2. Select "MCP" or "GitHub Copilot" from dropdown
3. Look for error messages

### Issue 2: Python Path Issues

**Test Path Validity:**
```powershell
# Verify file exists
Test-Path "C:\Users\YourUsername\petprojects\luise-mcp-server\mcp_server.py"

# Test Python executable
python --version
```

**Use Full Python Path:**
```json
{
  "mcp.servers": {
    "luise-api": {
      "command": "C:\\Users\\YourUsername\\petprojects\\luise-mcp-server\\venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\YourUsername\\petprojects\\luise-mcp-server\\mcp_server.py"]
    }
  }
}
```

### Issue 3: Copilot Chat doesn't recognize @mcp

**Check MCP Extension Documentation:**
- Different extensions may use different syntax
- Try `@tools`, `@context`, or other prefixes
- Check extension settings for configuration options

**Alternative Approaches:**
1. **Direct Tool Commands**: Use Command Palette → "MCP: Execute Tool"
2. **Natural Language**: "Query my MCP server for profile data"
3. **Context Files**: Some extensions use file-based context

### Issue 4: Tools connect but fail to execute

**Test Server Independently:**
```powershell
# Run MCP Inspector to verify server works
npx @modelcontextprotocol/inspector python mcp_server.py
```

**Check Network Access:**
- Server needs internet access to reach `api.m365princess.com`
- Test API directly: visit `https://api.m365princess.com/profile` in browser

**Virtual Environment Issues:**
```powershell
# Ensure packages installed in correct environment
.\venv\Scripts\Activate.ps1
pip list | findstr mcp
```

### Issue 5: VS Code Workspace Problems

**Workspace Configuration:**
```json
// In .vscode/settings.json
{
  "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
  "mcp.servers": {
    "luise-api": {
      "command": "${workspaceFolder}/venv/Scripts/python.exe",
      "args": ["${workspaceFolder}/mcp_server.py"]
    }
  }
}
```

## Multiple Environment Configuration

For development vs. production setups:

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

## Success Indicators

**✅ When everything works correctly:**

**In VS Code:**
- MCP-related commands in Command Palette
- MCP status indicators (extension dependent)
- No errors in Output panels

**In GitHub Copilot Chat:**
- `@mcp` commands are recognized (or alternative syntax)
- AI responds with actual Luise API data
- Formatted responses with emojis and structure
- Natural conversation flow about Luise's background

**In Server Logs** (if running manually):
- "Making API request to..." messages
- HTTP 200 status codes
- No error exceptions

## Next Steps

Once integrated successfully, explore:

1. **Natural Conversations**: Ask complex questions that span multiple API calls
2. **Contextual Queries**: Reference previous API results in follow-up questions  
3. **Development Integration**: Use MCP data in your coding workflow
4. **Custom Extensions**: Build your own MCP integrations for VS Code

Proceed to [Troubleshooting Guide](06-troubleshooting.md) for comprehensive problem-solving resources.

---

**[← Previous: Testing & Validation](04-testing.md)** | **[Next: Troubleshooting Guide →](06-troubleshooting.md)**