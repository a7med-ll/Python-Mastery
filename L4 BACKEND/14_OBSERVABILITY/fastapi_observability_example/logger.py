"""
Structured application logger.

Responsible for:
- Creating JSON logs
- Capturing application events
- Capturing request events
"""

import logging
import json
from datetime import datetime

# -----------------------------------------------------------------------------
# Custom JSON Log Formatter
# -----------------------------------------------------------------------------

class l4_015JSONFormatter(logging.Formatter):
    """Convert normal Python logs into structured JSON logs."""

    def format(self, record) -> str:
        """Format record to a structured JSON log."""

        log_data = {
            "timestamp": datetime.utcnow().isoformat(),

            "level": record.levelname,

            "service": "fastapi-observability",

            "message": record.getMessage(),
        }

        # ---------------------------------------------------------------------
        # Add dynamic fields from extra={}
        # ---------------------------------------------------------------------

        extra_fields = {
            "method",
            "path",
            "status_code",
            "duration_ms",
        }

        for field in extra_fields:

            if hasattr(record, field):

                log_data[field] = getattr(record, field)

        return json.dumps(
            log_data,
            indent=4
        )

# -----------------------------------------------------------------------------
# Logger Creation
# -----------------------------------------------------------------------------

def l4_015CreateLogger() -> logging.Logger:
    """ Create application logger."""

    logger = logging.getLogger("fastapi-observability")

    # Define minimum log level.
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers.
    if not logger.handlers:

        # Send logs to terminal.
        console_handler = logging.StreamHandler()

        # Apply JSON formatter.
        console_handler.setFormatter(l4_015JSONFormatter())

        # Attach handler.
        logger.addHandler(console_handler)

    return logger

# -----------------------------------------------------------------------------
# Global Application Logger
# -----------------------------------------------------------------------------

application_logger = l4_015CreateLogger()