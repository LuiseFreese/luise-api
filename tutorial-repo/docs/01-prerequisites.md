# Prerequisites & Setup (Windows)

This guide will help you set up your Windows development environment for building MCP servers.

## System Requirements (Windows Only)

- **Windows 10 or 11** (64-bit)
- **Python 3.11 or 3.12** from [python.org](https://python.org/downloads)
- **PowerShell** or **Command Prompt**
- **Visual Studio Code** (recommended for development)
- **Basic understanding** of Python and APIs (we'll guide you through everything else!)

## Step 1: Install Python (If Not Already Installed)

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

## Step 2: Create Your Project Directory

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

## Step 3: Set Up Python Virtual Environment

**⚠️ IMPORTANT: Make sure you're in `C:\Users\YourUsername\petprojects\luise-mcp-server` before running these commands!**

```powershell
# Double-check you're in the right directory
Get-Location
# Should show: C:\Users\YourUsername\petprojects\luise-mcp-server

# Create virtual environment
python -m venv venv

# Verify the venv folder was created
Test-Path venv
# Should return: True

# Activate virtual environment (IMPORTANT: You'll need to do this every time)
.\venv\Scripts\Activate.ps1

# Your prompt should now show (venv) at the beginning like:
# (venv) PS C:\Users\YourUsername\petprojects\luise-mcp-server>
```

**🚨 Troubleshooting Activation Issues:**

If you get **"The term '.\venv\Scripts\Activate.ps1' is not recognized"**:

1. **Check you're in the right directory:**
   ```powershell
   Get-Location
   # Must show: C:\Users\YourUsername\petprojects\luise-mcp-server
   ```

2. **Check the venv folder exists:**
   ```powershell
   Test-Path venv
   Get-ChildItem
   # Should see a 'venv' folder in the list
   ```

3. **If execution policy error:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   # Then try activation again
   .\venv\Scripts\Activate.ps1
   ```

4. **Alternative activation methods:**
   ```powershell
   # Method 1: Without dot-slash
   venv\Scripts\Activate.ps1
   
   # Method 2: Full path
   & "C:\Users\$env:USERNAME\petprojects\luise-mcp-server\venv\Scripts\Activate.ps1"
   ```

## Step 4: Install Required Packages

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

## Step 5: Install Node.js for MCP Inspector (Essential for Testing)

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

## ✅ Verification Checklist

Before proceeding, make sure you have:

- [ ] Python 3.11+ installed and in PATH
- [ ] Virtual environment created and activated
- [ ] All Python packages installed without errors
- [ ] Node.js and MCP Inspector installed
- [ ] PowerShell execution policy set appropriately

## 🚨 Common Setup Issues

**Issue: "Python is not recognized"**
- Solution: Reinstall Python with "Add to PATH" checked
- Or manually add Python to your system PATH

**Issue: "Execution policy error"**
- Solution: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Issue: "pip install fails"**
- Solution: Upgrade pip first: `python -m pip install --upgrade pip`

## Next Steps

Once your environment is set up, proceed to [Project Setup](02-project-setup.md) to create your MCP server structure.

---

**[← Back to README](../README.md)** | **[Next: Project Setup →](02-project-setup.md)**