import sys
from exoscan.lib.controls.compute.instances.inventory import get_instances
from exoscan.lib.controls.compute.elastic_ip.inventory import get_elastic_ip
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_eip_unused")
    try: 
        all_instances = get_instances()
        all_ips = get_elastic_ip()
        if not all_ips: 
            logger.info("No elastic IPs found. Skipping Control compute_eip_unused...")
            return
        findings = []
        unused_ips = []
        for ip in all_ips.elastic_ips:
            unused_ips.append(ip.ip) #assume all keys are unused
        
            for instance in all_instances.instances:
                for instance_ip in instance.elastic_ips:
                    if str(instance_ip.ip) == str(ip.ip):
                        if ip.ip in unused_ips:
                            unused_ips.remove(ip.ip)
                            break
  
        if unused_ips:
            eip_str = "\n - ".join(set(unused_ips))
            findings.append(Finding.from_metadata(
                        metadata_file= metadata_path,
                        resource_description=f"Elastic-IPs:\n - {eip_str}" #set to remove duplicates
                    ))
        return findings
                
    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return