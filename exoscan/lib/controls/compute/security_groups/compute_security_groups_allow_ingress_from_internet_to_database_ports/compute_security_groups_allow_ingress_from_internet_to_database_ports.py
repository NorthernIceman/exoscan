import sys
from exoscan.lib.controls.compute.security_groups.inventory import get_security_groups
from exoscan.lib.controls.models import SecurityGroupRule, SecurityGroupContainer, SecurityGroup
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_security_groups_allow_ingress_from_internet_to_database_ports")
    try: 
        all_sg = get_security_groups()
        if not all_sg.security_groups: 
            logger.info("No Security-Groups found. Skipping Control compute_security_groups_allow_ingress_from_internet_to_database_ports...")
            return
        findings = []
        risky_ports = [27017, 27018, 7199, 9160, 8888, 9092, 11211, 3306, 1521, 2483, 5432, 6379, 1433, 1434]
        for sg in all_sg.security_groups:
            risky_rules = []
            for rule in sg.rules:
                if rule.network and rule.start_port and rule.end_port: 
                    conf_risky_ports = []
                    for port in risky_ports: 
                        if (rule.network == "0.0.0.0/0" or "::0/0") and (port in range(int(rule.start_port), int(rule.end_port))) and rule.protocol == "tcp":
                            conf_risky_ports.append(port)
                    if conf_risky_ports: risky_rules.append(f"(Rule-ID: {rule.id}, Port: {str(conf_risky_ports)})")
            if risky_rules:             
                findings.append(Finding.from_metadata(
                    metadata_file= metadata_path,
                    resource_description=f"Security-Group: {sg.name} {str(risky_rules)}"
                ))
        return findings
                
    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return