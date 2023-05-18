import logging

logger = logging.getLogger("library_report")
logger.setLevel(logging.INFO)  # Set the logging level to INFO

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Set the logging level to INFO

# Create a formatter and add it to the console handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)
