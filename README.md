# Luise API

A playful REST API that serves as a personal introduction

## Features

- **Personal Profile API** - Get to know Luise
- **Skills & Expertise** - Technical skills with domain filtering and detailed information
- **Speaking History** - Past talks with detailed information
- **Project Portfolio** - Current and past open-source projects with architectural details

## Tech Stack

- **Python 3.11+** - Modern Python with type hints throughout
- **FastAPI** - High-performance async web framework
- **Pydantic v2** - Data validation and serialization
- **Uvicorn** - ASGI server for production-ready deployment
- **Pytest** - Comprehensive testing suite

## 🏃Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (or create the project structure):
   ```bash
   git clone https://github.com/example/luise-api.git
   cd luise-api
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Open your browser** and navigate to:
   - **API Documentation**: http://127.0.0.1:8000/docs
   - **Landing Page**: http://127.0.0.1:8000

## API Endpoints

### Profile Endpoints
- `GET /profile` - Get profile information

### Skills Endpoints
- `GET /skills` - List all skills with optional domain filtering

### Talks Endpoints
- `GET /talks` - List talks with optional year filtering

### Projects Endpoints
- `GET /projects` - List all projects

### System Endpoints
- `GET /health` - Health check
- `GET /` - API documentation (Swagger UI)


## Example Usage

### Basic Profile Request
```bash
curl "http://127.0.0.1:8000/profile"
```

### Filter Skills by Domain
```bash
curl "http://127.0.0.1:8000/skills?domain=AI"
```

### Get Talks from Specific Year
```bash
curl "http://127.0.0.1:8000/talks?year=2025"
```

### Get All Projects
```bash
curl "http://127.0.0.1:8000/projects"
```

### Health Check
```bash
curl "http://127.0.0.1:8000/health"
```

## Running Tests

Run the test suite to ensure everything works correctly:

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage  
python -m pytest tests/ --cov=app

# Run specific test file
python -m pytest tests/test_api.py -v
```


## 🔍 Architecture Highlights

### Clean Architecture Patterns
- **Separation of Concerns**: Models, services, and routers are cleanly separated
- **Dependency Injection**: Services are injected at the module level
- **Type Safety**: Comprehensive type hints throughout the codebase

### Error Handling
- **Consistent Error Format**: All errors follow the same JSON structure
- **Proper HTTP Status Codes**: Meaningful status codes for different scenarios
- **Detailed Error Messages**: Helpful error messages with context

### API Design
- **Read-Only**: Clean, safe GET-only endpoints
- **RESTful**: Follows REST conventions and best practices
- **Filtered Queries**: Support for domain/year filtering where appropriate

## 🚀 Deployment

For production deployment, consider:

```bash
# Production server with Gunicorn
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Or using Uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📝 Development Notes

### Code Style
- Type hints throughout the codebase
- Consistent naming conventions
- Comprehensive docstrings
- Clean separation between business logic and API routes

### Design Decisions
- **Read-Only API**: Clean GET-only methods for safe, simple demonstration
- **No Database**: Uses JSON files for easy setup and portability
- **Streamlined Endpoints**: Focused on essential functionality only
- **Error Handling**: Consistent error response format across all endpoints
- **Data Validation**: Leverages Pydantic v2 for comprehensive request/response validation
- **Modern Python**: Uses latest Pydantic patterns and type hints

## 🤝 Contributing

This is a demo project, but if you'd like to suggest improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add or update tests
5. Submit a pull request

## 📄 License

MIT License - feel free to use this code as inspiration for your own projects!

---

**Built with ❤️ **