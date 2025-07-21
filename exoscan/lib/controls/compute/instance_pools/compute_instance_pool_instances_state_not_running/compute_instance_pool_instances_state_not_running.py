import sys
from exoscan.lib.controls.compute.instance_pools.inventory import get_instance_pools
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_instance_pool_instances_state_not_running")
    try: 
        all_instance_pools = get_instance_pools()
        if not all_instance_pools.instance_pools: 
            logger.info("No instance-pools found. Skipping Control compute_instance_pool_instances_state_not_running...")
            return

        findings = []
        found_instance_pools = []
        found_instances = []
        for instance_pool in all_instance_pools.instance_pools:
            if not instance_pool.instances:
                break
            for instance in instance_pool.instances:
                if instance.state != "running":
                     found_instances.append(instance.name)
            if found_instances:
                 instance_str = f"\n     ".join(found_instances)
                 found_instance_pools.append(f" - Instance-Pool: {instance_pool.name}\n    Instances:\n     {instance_str}")

                     
        if found_instance_pools:
                instance_pool_str = "\n - ".join(found_instance_pools)
                findings.append(Finding.from_metadata(
                    metadata_file= metadata_path,
                    resource_description=f"Instance-Pools: \n{str(instance_pool_str)}"
                ))
        return findings

    except Exception as error:
        logger.error(f"1{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return