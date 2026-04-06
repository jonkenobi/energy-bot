import logging
import os

def setup_logging():
    os.makedirs("logs", exist_ok=True)  # creates logs/ if it doesn't exist

    log_formatter = logging.Formatter(
        fmt="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S"
    )

    file_handler = logging.FileHandler("logs/system_events.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_formatter)

    for name in ["reliability.retry", "reliability.circuit_breaker", "price_feed", "adr.handler"]:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.propagate = False

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)