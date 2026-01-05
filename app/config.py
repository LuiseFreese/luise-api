import os
from typing import Optional

class Settings:
    app_name: str = "Luise API"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # CORS settings for production
    cors_origins: list = [
        "https://m365princess.com",
        "https://www.m365princess.com"
    ]
    
    # Security
    allowed_hosts: list = ["*"]  # Restrict this in production
    
settings = Settings()