import sys
from exoscan.lib.controls.compute.instances.inventory import get_instances
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger
from pathlib import Path
from datetime import datetime, timedelta, timezone

def execute_logic(metadata_path):
    logger.info("Executing control: compute_instance_older_than_specific_days")
    try: 
        all_instances = get_instances()
        if not all_instances.instances: 
            logger.info("No instances found. Skipping Control compute_instance_older_than_specific_days...")
            return
        threshold = datetime.now(timezone.utc) - timedelta(days=90)
        findings = []
        found_instances = []
        for instance in all_instances.instances:
            if instance.created_at < threshold:
                found_instances.append(instance.id)
        if found_instances:
            instances_str = "\n - ".join(found_instances)
            findings.append(Finding.from_metadata(
                metadata_file= metadata_path,
                resource_description=f"Instances: \n - {str(instances_str)}"
            ))
        return findings

    except Exception as error:
        logger.error(f"1{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return