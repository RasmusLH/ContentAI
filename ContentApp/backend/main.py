import uvicorn
from app.appmain import app
from app.utils.logging_config import setup_logging  # Import logging setup

if __name__ == "__main__":
    setup_logging()  # Initialize logging before starting uvicorn
    uvicorn.run(
        "app.appmain:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None,  # Disable uvicorn’s default logging config
        log_level="info",
        access_log=True
    )
