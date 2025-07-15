import sys
from exoscan.lib.controls.compute.instances.inventory import get_instances
from exoscan.lib.controls.compute.ssh_keys.inventory import get_ssh_keys
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_ssh_keys_unused")
    try: 
        all_instances = get_instances()
        all_keys = get_ssh_keys()
        if not all_keys: 
            logger.info("No Keys found. Skipping Control compute_ssh_keys_unused...")
            return
        findings = []
        unused_keys = []
        for key in all_keys.ssh_keys:
            unused_keys.append(key.name) #assume all keys are unused
        
            for instance in all_instances.instances:
                for instance_key in instance.ssh_keys:
                    if str(instance_key.name) == str(key.name):
                        if key.name in unused_keys:
                            unused_keys.remove(key.name)
                            break
  
        if unused_keys:
            sshkey_str = "\n - ".join(set(unused_keys))
            findings.append(Finding.from_metadata(
                        metadata_file= metadata_path,
                        resource_description=f"SSH-Keys:\n - {sshkey_str}" #set to remove duplicates
                    ))
        return findings
                
    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return