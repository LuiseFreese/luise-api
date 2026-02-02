# Configuration Examples

This directory contains example configuration files for integrating your MCP server with various tools.

## VS Code Settings

### User Settings (Global)
**File:** `vscode-user-settings.json`
**Location:** Copy content to your VS Code User Settings
- Windows: `%APPDATA%\Code\User\settings.json`
- Or: VS Code → File → Preferences → Settings → Open Settings (JSON)

**Usage:**
- Global configuration across all VS Code projects
- Replace `YourUsername` with your actual Windows username
- Requires absolute paths to your MCP server

### Workspace Settings (Project-Specific) 
**File:** `vscode-workspace-settings.json`
**Location:** Copy content to `.vscode/settings.json` in your project root

**Usage:**
- Project-specific configuration
- Uses relative paths with `${workspaceFolder}` variable
- Better for sharing projects or version control

## Path Configuration Examples

### Windows Path Examples

**Standard User:**
```json
"args": ["C:\\Users\\john\\petprojects\\luise-mcp-server\\mcp_server.py"]
```

**User with Spaces in Name:**
```json
"args": ["C:\\Users\\John Smith\\petprojects\\luise-mcp-server\\mcp_server.py"]
```

**Corporate Domain User:**
```json
"args": ["C:\\Users\\john.smith\\petprojects\\luise-mcp-server\\mcp_server.py"]
```

### Virtual Environment Paths

**Using Virtual Environment Python:**
```json
{
  "command": "C:\\Users\\YourUsername\\petprojects\\luise-mcp-server\\venv\\Scripts\\python.exe",
  "args": ["C:\\Users\\YourUsername\\petprojects\\luise-mcp-server\\mcp_server.py"]
}
```

**Using System Python:**
```json
{
  "command": "python",
  "args": ["C:\\Users\\YourUsername\\petprojects\\luise-mcp-server\\mcp_server.py"]
}
```

## Environment Variables

### Development vs Production

**Development Configuration:**
```json
{
  "env": {
    "API_BASE_URL": "https://api.m365princess.com",
    "LOG_LEVEL": "DEBUG",
    "TIMEOUT": "30"
  }
}
```

**Production Configuration:**
```json
{
  "env": {
    "API_BASE_URL": "https://api.m365princess.com", 
    "LOG_LEVEL": "INFO",
    "TIMEOUT": "10"
  }
}
```

## Multiple Server Configuration

**Running Multiple MCP Servers:**
```json
{
  "mcp.servers": {
    "luise-api": {
      "command": "python",
      "args": ["C:\\Path\\To\\luise-mcp-server\\mcp_server.py"],
      "env": {
        "API_BASE_URL": "https://api.m365princess.com"
      }
    },
    "weather-api": {
      "command": "python",
      "args": ["C:\\Path\\To\\weather-mcp-server\\server.py"],
      "env": {
        "WEATHER_API_KEY": "your-api-key"
      }
    },
    "local-filesystem": {
      "command": "python",
      "args": ["C:\\Path\\To\\filesystem-mcp-server\\server.py"],
      "env": {
        "ROOT_PATH": "C:\\Users\\YourUsername\\Documents"
      }
    }
  }
}
```

## Troubleshooting Configuration

### Debug Configuration
For maximum debugging information:

```json
{
  "mcp.servers": {
    "luise-api-debug": {
      "command": "python",
      "args": ["-u", "C:\\Path\\To\\mcp_server.py"],
      "env": {
        "API_BASE_URL": "https://api.m365princess.com",
        "LOG_LEVEL": "DEBUG",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Flags Explained:**
- `-u`: Unbuffered Python output (immediate logging)
- `PYTHONUNBUFFERED=1`: Same as `-u` but via environment variable
- `LOG_LEVEL=DEBUG`: Maximum log verbosity

### Network Issues Configuration
For corporate environments with proxies:

```json
{
  "env": {
    "API_BASE_URL": "https://api.m365princess.com",
    "HTTP_PROXY": "http://your-proxy:8080", 
    "HTTPS_PROXY": "http://your-proxy:8080",
    "NO_PROXY": "localhost,127.0.0.1"
  }
}
```

## Configuration Validation

### Quick Test Command
Test your configuration with:

```powershell
# Navigate to your MCP server directory
cd C:\Users\YourUsername\petprojects\luise-mcp-server

# Test server startup manually
python mcp_server.py
# Should start without errors

# Test with same path as VS Code config
"C:\Users\YourUsername\petprojects\luise-mcp-server\venv\Scripts\python.exe" "C:\Users\YourUsername\petprojects\luise-mcp-server\mcp_server.py"
```

### JSON Validation
Always validate your JSON configuration:
1. Copy settings to [jsonlint.com](https://jsonlint.com)
2. Fix any syntax errors (common: trailing commas, unescaped backslashes)
3. Test in VS Code

### Path Testing
Verify paths exist:

```powershell
# Test Python executable
Test-Path "C:\Users\YourUsername\petprojects\luise-mcp-server\venv\Scripts\python.exe"

# Test MCP server file
Test-Path "C:\Users\YourUsername\petprojects\luise-mcp-server\mcp_server.py"

# Should both return: True
```

## Extension Compatibility

### Known Working Extensions
- **GitHub Copilot**: Official Microsoft extension
- **MCP Client**: Various community extensions (check marketplace)

### Extension Settings
Some MCP extensions may require additional settings:

```json
{
  "mcp.autostart": true,
  "mcp.timeout": 30000,
  "mcp.retries": 3,
  "github.copilot.advanced": {
    "debug.overrideEngine": "mcp-enhanced"
  }
}
```

**Note:** Extension-specific settings vary by extension. Check documentation for your chosen MCP extension.

---

Use these configuration examples as starting points and modify paths and settings according to your specific setup and requirements.