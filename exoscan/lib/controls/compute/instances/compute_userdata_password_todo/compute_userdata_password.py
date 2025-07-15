import sys
from exoscan.lib.controls.compute.instances.inventory import get_instances
from exoscan.lib.controls.models import Instance, InstanceContainer
from log_conf.logger import logger

def execute_logic(metadata_path):
    #logger.info("Executing Control: compute_public_instance_unrestricted_ingress")
    try: 
        all_instances = get_instances()
        if not all_instances.instances: 
            logger.info("No instances found. Skipping Control compute_public_instance...")
            return
        #TODO: check for password in user_data

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return