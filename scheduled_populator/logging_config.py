import logging
import os

# Create a logs directory if it doesn't exist
if not os.path.exists('scheduled_populator/logs'):
    os.makedirs('scheduled_populator/logs')

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduled_populator/logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)