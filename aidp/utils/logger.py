import structlog
import logging

def configure_logger():
    """Configure structlog for JSON line output.

    This function is idempotent; calling it multiple times has no adverse effect.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(asctime)s %(name)s %(message)s",
    )
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

# Initialize logger on import
configure_logger()

def get_logger(name: str = __name__):
    """Return a structlog logger bound to the given name."""
    return structlog.get_logger(name)
