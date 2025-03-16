import logging
import json
import sys
from datetime import datetime
from ..config import settings

class JSONFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.fromtimestamp(record.created).isoformat()
        json_record = {
            "timestamp": timestamp,
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "path": getattr(record, 'path', None)
        }
        
        if hasattr(record, 'extra'):
            json_record.update(record.extra)
        
        if record.exc_info:
            json_record['exc_info'] = self.formatException(record.exc_info)
            
        return json.dumps(json_record)

def setup_logging():
    # Clear all existing handlers
    logging.getLogger().handlers = []
    
    # Basic configuration
    logging.basicConfig(
        level=settings.log_level,
        format=settings.log_format,
        stream=sys.stdout,
        force=True  # Override any existing configuration
    )
    
    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level)
    
    # Add JSON handler for all app loggers
    json_handler = logging.StreamHandler(sys.stdout)
    json_handler.setFormatter(JSONFormatter())
    json_handler.setLevel(settings.log_level)
    
    # Configure specific loggers
    loggers = [
        "uvicorn",
        "uvicorn.access",
        "fastapi",
        "app",
        "__main__"
    ]
    
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.handlers = []  # Clear existing handlers
        logger.addHandler(json_handler)
        logger.setLevel(settings.log_level)
        logger.propagate = True  # Allow logs to bubble up to root logger
    
    # Test logging
    root_logger.info("Logging system initialized", extra={"logger_setup": "complete"})
