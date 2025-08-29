import sys
from exoscan.lib.controls.compute.security_groups.inventory import get_security_groups
from exoscan.lib.controls.compute.instances.inventory import get_instances
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_sg_unused_group")
    try: 
        all_instances = get_instances()
        all_sg = get_security_groups()
        if not all_sg.security_groups: 
            logger.info("No Security-Groups found. Skipping Control compute_sg_unused_group...")
            return
        findings = []
        unused_sg = []
        for sg in all_sg.security_groups:
            if sg.name == "default": continue #the default security group is always present and cannot be deleted
            unused_sg.append(sg.name) #assume all sg are unused
        
            for instance in all_instances.instances:
                if str(sg.id) in str(instance.security_groups) or not instance.security_groups:
                    unused_sg.remove(sg.name) #if sg is used by an instance, remove it from the unused list
                    break
  
        if unused_sg:
            findings.append(Finding.from_metadata(
                        metadata_file= metadata_path,
                        resource_description=f"Security-Group: {str(set(unused_sg))}" #set to remove duplicates
                    ))
        return findings
                
    except Exception as error:
        logger.error(f"1{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error} {unused_sg}")
        sys.exit(1)
    return