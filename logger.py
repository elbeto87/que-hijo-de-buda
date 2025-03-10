import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
