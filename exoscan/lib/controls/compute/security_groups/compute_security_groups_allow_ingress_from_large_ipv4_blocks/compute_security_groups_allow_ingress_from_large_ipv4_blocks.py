import sys
from exoscan.lib.controls.compute.security_groups.inventory import get_security_groups
from exoscan.lib.controls.models import SecurityGroupRule, SecurityGroupContainer, SecurityGroup
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_security_groups_allow_ingress_from_large_ipv4_blocks")
    try: 
        all_sg = get_security_groups()
        if not all_sg.security_groups: 
            logger.info("No Security-Groups found. Skipping Control compute_security_groups_allow_ingress_from_large_ipv4_blocks...")
            return
        findings = []
        prefix_threshold = "24"
        found_sg = []
        for sg in all_sg.security_groups:
            risky_rules = []
            for rule in sg.rules:
                if rule.network != None and rule.flow_direction == "ingress" and not (rule.network.startswith("10.") or rule.network.startswith("172.") or rule.network.startswith("192.168.")): 
                    prefix = rule.network.split('/')[1]
                    if prefix <= prefix_threshold and not "0": #not 0 cause there is another control doing this
                        risky_rules.append(f"(Rule-ID: {rule.id})")
            if risky_rules:     
                rules_str = "\n    ".join(risky_rules)
                found_sg.append(f" - Security-Group: {sg.name}\n    {rules_str}")
        if found_sg:
            sgs_str = "\n".join(found_sg)
            findings.append(Finding.from_metadata(
                metadata_file= metadata_path,
                resource_description=f"Security-Group:\n{sgs_str}"
            ))
        return findings
                
    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return