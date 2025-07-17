import sys
from exoscan.lib.controls.compute.instances.inventory import get_instances
from exoscan.lib.controls.models import Finding
from collections import defaultdict
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing control: compute_instance_majority_in_same_zone")
    try: 
        all_instances = get_instances()
        if not all_instances.instances: 
            logger.info("No instances found. Skipping Control compute_instance_majority_in_same_zone...")
            return

        findings = []
        region_counter = defaultdict(list)
        for instance in all_instances.instances:
            region_counter[instance.region].append(instance.id)

        total_instances = len(all_instances.instances)

        max_region = None
        max_count = 0
        for region, instances in region_counter.items():
            if len(instances) > max_count:
                max_count = len(instances)
                max_region = region

        percentage = (max_count / total_instances) * 100
        if percentage >= 80:
            instances_str = "\n - ".join(region_counter[max_region])
            findings.append(Finding.from_metadata(
                metadata_file=metadata_path,
                resource_description=(
                    f"Region '{max_region}' hosts {max_count}/{total_instances} instances "
                    f"({percentage:.2f}%).\nInstances:\n - {instances_str}"
                )
            ))

        return findings


    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return