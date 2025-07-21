import sys
from exoscan.lib.controls.compute.instances.inventory import get_instances
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_instance_no_anti_affinity_group")
    try: 
        all_instances = get_instances()
        if not all_instances.instances: 
            logger.info("No instances found. Skipping Control compute_instance_no_anti_affinity_group...")
            return

        findings = []
        found_instances = []

        for instance in all_instances.instances:
            if not instance.anti_affinity_groups:
                found_instances.append(instance.name)
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