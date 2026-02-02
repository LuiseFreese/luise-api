# Building Your First MCP Server: Complete Tutorial

*Connect any REST API to AI assistants like GitHub Copilot through the Model Context Protocol*

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Platform-Windows-lightgrey.svg" alt="Windows">
  <img src="https://img.shields.io/badge/MCP-Protocol-green.svg" alt="MCP Protocol">
  <img src="https://img.shields.io/badge/AI-Assistant-orange.svg" alt="AI Assistant">
</p>

## 🚀 What You'll Build

By the end of this tutorial, you'll have created a complete MCP (Model Context Protocol) server that allows AI assistants like GitHub Copilot to naturally query and interact with REST APIs through conversation. 

**Example interaction:**
```
You: "Tell me about Luise's cloud expertise"
AI Assistant: 🚀 Technical Skills (Domain: cloud):

**Azure** - Expert
Microsoft Azure cloud platform with extensive experience in...

**AWS** - Advanced  
Amazon Web Services for scalable cloud solutions...
```

## 📋 What You'll Learn

- **MCP Protocol fundamentals** - How AI assistants discover and use external tools
- **Tool design patterns** - Converting API endpoints into AI-usable functions
- **Async API integration** - Proper HTTP client usage with error handling
- **Response formatting** - Making API data conversational and readable
- **Testing strategies** - Both automated testing and interactive debugging
- **AI assistant integration** - Connecting your server to GitHub Copilot in VS Code

## 🎯 Real-World Example

This tutorial uses the **Luise API** (a real FastAPI service at `api.m365princess.com`) as our example, but the patterns work with **any REST API**:

- Your own personal/portfolio API
- Company internal services  
- Public APIs (GitHub, weather, news, etc.)
- Any HTTP-based data source

## 🛠️ Prerequisites

- **Windows 10/11** (64-bit)
- **Python 3.11+** from [python.org](https://python.org/downloads)
- **VS Code** with GitHub Copilot
- **Node.js** for MCP Inspector testing tool
- **Basic Python knowledge** (we'll guide you through everything else!)

## 📚 Tutorial Structure

### 📖 **Documentation**
1. **[Prerequisites & Setup](docs/01-prerequisites.md)** - Windows environment setup
2. **[Project Setup](docs/02-project-setup.md)** - Creating your project structure  
3. **[Building the MCP Server](docs/03-mcp-server.md)** - Complete server implementation
4. **[Testing & Validation](docs/04-testing.md)** - Testing with MCP Inspector
5. **[GitHub Copilot Integration](docs/05-integration.md)** - Connecting to VS Code
6. **[Troubleshooting Guide](docs/06-troubleshooting.md)** - Common issues and solutions

### 💻 **Code**
- **[Complete MCP Server](src/mcp_server.py)** - Ready-to-run implementation
- **[Automated Tests](src/test_mcp.py)** - Comprehensive test suite
- **[Configuration Examples](config/)** - VS Code settings and more

### 🎯 **Examples**
- **[Basic API Example](examples/basic-api/)** - Simpler starting point
- **[Advanced Features](examples/advanced/)** - Extended functionality

## ⚡ Quick Start

```powershell
# Clone the repository
git clone https://github.com/yourusername/mcp-server-tutorial.git
cd mcp-server-tutorial

# Set up environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Test the server
python src/mcp_server.py
```

Then follow the [integration guide](docs/05-integration.md) to connect it to GitHub Copilot!

## 🌟 Key Features

- **🔧 Complete Working Example** - Not just theory, but a real MCP server you can run
- **🪟 Windows-First** - Designed specifically for Windows developers  
- **🤖 GitHub Copilot Ready** - Integrates seamlessly with VS Code
- **🧪 Comprehensive Testing** - Both automated and interactive testing approaches
- **🛠️ Troubleshooting** - Detailed solutions for common Windows issues
- **📦 Adaptable Code** - Easy to modify for your own APIs

## 🎭 What Makes This Different

Unlike basic MCP examples, this tutorial covers:

- ✅ **Real error handling** for production use
- ✅ **Windows-specific setup** and troubleshooting  
- ✅ **Complete testing strategy** with MCP Inspector
- ✅ **Natural conversation flow** with formatted responses
- ✅ **Practical deployment** considerations

## 🤝 Contributing

Found an issue? Want to add support for another platform? Contributions welcome!

- 🐛 **Report bugs** via GitHub Issues
- 💡 **Suggest improvements** or additional examples
- 🔧 **Submit PRs** for fixes or new features
- 📚 **Improve documentation** 

## 📄 License

MIT License - feel free to use this for your own projects!

## 🔗 Related Resources

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Inspector Tool](https://github.com/modelcontextprotocol/inspector)
- [GitHub Copilot Documentation](https://docs.github.com/copilot)

---

**Ready to get started?** Head to [Prerequisites & Setup](docs/01-prerequisites.md) to begin building your first MCP server! 🚀