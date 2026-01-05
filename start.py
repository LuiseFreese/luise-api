#!/usr/bin/env python3
"""Production startup script for the Luise API."""

import uvicorn
import os

if __name__ == "__main__":
    # Railway provides PORT, fallback to 8000 for local development
    port = int(os.environ.get("PORT", "8000"))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False,
        access_log=True
    )