from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import profile, skills, talks, projects, debug

# OpenAPI configuration
app = FastAPI(
    title="Luise API",
    description="""
A playful REST API that serves as a personal introduction and a demonstration 
of FastAPI best practices. 

## Features

- **Comprehensive Profile Information** - Get to know Luise
- **Skills & Expertise** - Detailed technical skills with filterable domains  
- **Speaking History** - Past talks and presentations with
- **Project Portfolio** - Current and past projects with architecture details

## API Design Principles

- Consistent error responses with helpful details
- Comprehensive request/response validation
- Rate limiting on selected endpoints
- Proper HTTP status codes and semantics
- Interactive documentation with examples
    """,
    version="1.0.0",
    contact={
        "name": "Luise",
        "url": "https://github.com/example/luise-api",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    swagger_ui_parameters={
        "defaultModelsExpandDepth": 2,
        "defaultModelExpandDepth": 2,
        "displayRequestDuration": True,
        "docExpansion": "list",
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
    },
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Add CORS middleware for public access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://m365princess.com",
        "https://www.m365princess.com",
        "https://api.m365princess.com",
        "*"  # Remove this in production for better security
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Now allowing POST for talk questions
    allow_headers=["*"],
)

# Mount static files for custom CSS and assets
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers with their configured prefixes and tags
app.include_router(profile.router)
app.include_router(skills.router)
app.include_router(talks.router)
app.include_router(projects.router)
app.include_router(debug.router)


@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint that redirects to the API documentation."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")


@app.get("/health", include_in_schema=False)
async def health_check():
    """Simple health check endpoint for monitoring."""
    return {"status": "healthy", "service": "luise-api"}


# Configure custom Swagger UI with pink theme
def custom_openapi():
    """Custom OpenAPI configuration."""
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    
    openapi_schema = get_openapi(
        title="Luise API",
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )
    
    # Add custom styling info to OpenAPI spec
    openapi_schema["info"]["x-logo"] = {
        "url": "/static/logo.png",
        "altText": "Luise API Logo"
    }
    
    # Add tag descriptions
    openapi_schema["tags"] = [
        {
            "name": "Profile",
            "description": "Personal information and profile details"
        },
        {
            "name": "Skills", 
            "description": "Technical skills and expertise areas with domain filtering"
        },
        {
            "name": "Talks",
            "description": "Speaking engagements and presentations"
        },
        {
            "name": "Projects",
            "description": "Portfolio projects with architecture details and tech stacks"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Add custom CSS to Swagger UI
@app.get("/docs", response_class=HTMLResponse, include_in_schema=False)  
async def custom_swagger_ui_html():
    """Custom Swagger UI with pink theme."""
    from fastapi.openapi.docs import get_swagger_ui_html
    
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Interactive API Documentation",
        swagger_css_url="/static/swagger-custom.css"
    )