import sys
from exoscan.lib.controls.compute.instances.inventory import get_instances
from exoscan.lib.controls.compute.security_groups.inventory import get_security_groups
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_instance_public_ingress_all_ports")
    try: 
        all_instances = get_instances()
        if not all_instances.instances: 
            logger.info("No instances found. Skipping Control compute_instance_public_ingress_all_ports...")
            return
        
        findings = []
        found_instances = []

        for instance in all_instances.instances:
            if instance.public_ip_assignment != "none": #security groups cannot be attached to private instances, but maybe they change this someday
                sglist = instance.security_groups
                found_sg = []
                for sg in sglist:
                    if sg: 
                        examined_sg = get_security_groups(sg.id)
                        if examined_sg.rules:
                            found_rule = []
                            for rule in examined_sg.rules:
                                if (rule.network == "0.0.0.0/0" or rule.network == "::/0") and rule.flow_direction == "ingress":
                                    if rule.start_port and rule.end_port: #if the rule has ports defined
                                        if rule.start_port == 1 and rule.end_port == 65535:
                                            found_rule.append(f"  (Rule-ID: {rule.id}")
                            if found_rule:
                                rules_str = "\n       ".join(found_rule)
                                found_sg.append(f"Security-Group: {examined_sg.name}\n      {rules_str}")
                if found_sg:
                    sgs_str = "\n    ".join(found_sg)
                    found_instances.append(f" - Instance: {instance.name}\n    {sgs_str}")

                        

        if found_instances:
            instances_str = "\n".join(found_instances)
            findings.append(Finding.from_metadata(
                metadata_file=metadata_path,
                resource_description=f"Instances:\n{instances_str}"
            ))
        return findings


    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return
