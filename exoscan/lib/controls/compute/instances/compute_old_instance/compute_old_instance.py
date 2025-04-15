import sys
from exoscan.lib.controls.compute.instances.inventory import get_instances
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger
from pathlib import Path
from datetime import datetime, timedelta, timezone

def execute_logic(metadata_path):
    
    try: 
        all_instances = get_instances()
        if not all_instances.instances: 
            logger.info("No instances found. Skipping Control compute_old_instance...")
            return
        threshold = datetime.now(timezone.utc) - timedelta(days=0)
        findings = []

        logger.info("Executing control: compute_old_instance")

        for instance in all_instances.instances:
            if instance.created_at < threshold:
                findings.append(Finding.from_metadata(
                    metadata_file= metadata_path,
                    resource_description=f"Instance {instance.name}"
                ))
        return findings
            
                #TODO: do stuff with metadata file (import it correctly)

    except Exception as error:
        logger.error(f"1{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return