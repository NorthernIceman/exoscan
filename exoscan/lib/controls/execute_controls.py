import importlib
from log_conf.logger import logger

def execute_controls(controls_modules_path):
    logger.info("Executing controls...")
    try: 
        for module in controls_modules_path:
            control = importlib.import_module(f"{module}")
            control.execute_logic()
    except Exception as error: 
        logger.error(
            f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}"
        )
