"""
Production-ready script to run the Uvicorn server for the Santander Customer Transaction App.

This script initializes the Uvicorn server to run the FastAPI application for the Santander Customer Transaction App in a production environment.
"""

from utils.config_reader import server_config, classification_config
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        # Run the application with Uvicorn
        uvicorn.run(
            "server.app:app",
            host=server_config["host"],
            port=server_config["port"],
            reload=False,  # Turn off auto-reload for production
            workers=4,  # Adjust the number of workers based on your system's capabilities
        )
    except Exception as e:
        logger.error(f"Failed to start the application: {e}")
