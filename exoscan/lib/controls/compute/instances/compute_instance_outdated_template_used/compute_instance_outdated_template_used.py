import sys
from exoscan.lib.controls.compute.instances.inventory import get_instances, get_instance_templates
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_instance_outdated_template_used")
    try: 
        all_instances = get_instances()
        if not all_instances.instances: 
            logger.info("No instances found. Skipping Control compute_instance_outdated_template_used...")
            return

        findings = []
        found_instances = []

        for instance in all_instances.instances:
            full_instance_template = get_instance_templates(instance.template.id)
            if full_instance_template == False: 
                found_instances.append(instance.name)

        if found_instances:
                instances_str = "\n - ".join(found_instances)
                findings.append(Finding.from_metadata(
                    metadata_file= metadata_path,
                    resource_description=f"Instances:\n - {str(instances_str)}"
                ))
        return findings

    except Exception as error:
        logger.error(f"1{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return