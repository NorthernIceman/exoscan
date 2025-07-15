import sys
from exoscan.lib.controls.compute.instances.inventory import get_instances
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger
from datetime import datetime, timedelta, timezone

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_ssh_keys_older_than_specific_days")
    try: 
        all_instances = get_instances()
        if not all_instances.instances: 
            logger.info("No instances found. Skipping Control compute_ssh_keys_older_than_specific_days...")
            return
        threshold = datetime.now(timezone.utc) - timedelta(days=180)    #every half year ssh-keys should be rotated, no recommendation from BSI
        findings = []
        old_keys = []
        for instance in all_instances.instances:
            if instance.created_at < threshold:
                if instance.ssh_key and instance.ssh_key.name:
                    old_keys.append(f"{instance.ssh_key.name}")
        if old_keys:
            sshkey_str = "\n - ".join(set(old_keys))
            findings.append(Finding.from_metadata(
                metadata_file= metadata_path,
                resource_description=f"SSH-Keys:\n - {sshkey_str}"
            ))
        return findings
                
    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return