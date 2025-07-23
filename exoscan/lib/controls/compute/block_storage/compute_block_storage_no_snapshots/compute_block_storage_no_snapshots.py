import sys
from exoscan.lib.controls.compute.block_storage.inventory import get_block_storage_volumes
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_block_storage_no_snapshots")
    try: 
        all_volumes = get_block_storage_volumes()
        if not all_volumes: 
            logger.info("No Volumes found. Skipping Control compute_block_storage_no_snapshots...")
            return
        findings = []
        unused_volumes = []
        for volume in all_volumes.block_storage_volumes:
            if not volume.block_storage_snapshots: 
                unused_volumes.append(volume.name) 
        
        if unused_volumes:
            volumes_str = "\n - ".join(set(unused_volumes))
            findings.append(Finding.from_metadata(
                        metadata_file= metadata_path,
                        resource_description=f"Volumes:\n - {volumes_str}" 
                    ))
        return findings
                
    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return