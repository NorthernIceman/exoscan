import sys
from exoscan.lib.controls.compute.instances.inventory import get_instances
from exoscan.lib.controls.compute.security_groups.inventory import get_security_groups
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_instance_public_ingress_kerberos_ldap_ports")
    try: 
        all_instances = get_instances()
        if not all_instances.instances: 
            logger.info("No instances found. Skipping Control compute_instance_public_ingress_kerberos_ldap_ports...")
            return
        
        findings = []
        found_instances = []
        risky_ports = [88, 464, 749, 750, 389, 636]

        for instance in all_instances.instances:
            if instance.public_ip_assignment != "none": #security groups cannot be attached to private instances, but maybe they change this someday
                sglist = instance.security_groups
                found_sg = []
                for sg in sglist:
                    if sg: 
                        examined_sg = get_security_groups(sg.id) #if it has a security group, get it
                        if examined_sg.rules: #if it has rules, check them
                            found_rule = []
                            for rule in examined_sg.rules:
                                if (rule.network == "0.0.0.0/0" or rule.network == "::/0") and rule.flow_direction == "ingress":
                                    if rule.start_port and rule.end_port: #if the rule has ports defined
                                        conf_risky_ports = []
                                        for port in risky_ports:
                                            if port in range(int(rule.start_port), int(rule.end_port) + 1) and rule.protocol == "tcp":
                                                conf_risky_ports.append(port)
                                        if conf_risky_ports:
                                            found_rule.append(f"(Rule-ID: {rule.id}, Port: {str(set(conf_risky_ports))})")
                            if found_rule:
                                rules_str = "\n      ".join(found_rule)
                                found_sg.append(f"Security-Group: {examined_sg.name}\n    {rules_str}")  
                if found_sg:
                    sgs_str = "\n    ".join(found_sg)
                    found_instances.append(f" - Instance: {instance.name}\n  {sgs_str}")
                                
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
