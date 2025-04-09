from exoscan.lib.controls.models import ControlMeta, Control
from log_conf.logger import logger


def fetch_controls(
        bulk_controls_meta: dict = None
) -> set: 

    logger.info("Fetching controls.")
    
    try:
        controls_to_execute = set()
        if not bulk_controls_meta:
            bulk_controls_meta = ControlMeta.get_all_controls()
        # for control_name in ControlMeta.list(bulk_controls_meta=bulk_controls_meta):
        #     controls_to_execute.add(control_name)
        
        return controls_to_execute
    except Exception as error:
        logger.error(
            f"1{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}"
        )
        return controls_to_execute