import sys
from exoscan.lib.controls.compute.instances.inventory import get_instances, get_instance_types
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_instance_large_instance_type")
    try: 
        all_instances = get_instances()
        if not all_instances.instances: 
            logger.info("No instances found. Skipping Control compute_instance_large_instance_type...")
            return

        findings = []
        found_instances = []
        large_instance_types = ["mega", "titan", "jumbo"] 

        for instance in all_instances.instances:
            full_instance_type = get_instance_types(instance.instance_type.id)

            if full_instance_type.size in large_instance_types and full_instance_type.gpus is not None:
                found_instances.append(f"\n - {instance.name} Size: {full_instance_type.size}  GPUs: {full_instance_type.gpus} Region: {instance.region}")
            if full_instance_type.size in large_instance_types:
                found_instances.append(f"\n - {instance.name} Size: {full_instance_type.size} Region: {instance.region}")
            if full_instance_type.gpus is not None:
                found_instances.append(f"\n - {instance.name} GPUs: {full_instance_type.gpus} Region: {instance.region}")
        if found_instances:
                instances_str = "".join(found_instances)
                findings.append(Finding.from_metadata(
                    metadata_file= metadata_path,
                    resource_description=f"Instances: {str(instances_str)}"
                ))
        return findings

    except Exception as error:
        logger.error(f"1{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return