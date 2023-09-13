from loguru import logger
import functions as fuc

logger.add("logs.log", level='INFO', colorize=False)

logger.info(f'START LOGGER')
