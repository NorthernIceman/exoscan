import sys
from exoscan.lib.controls.compute.security_groups.inventory import get_security_groups
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_sg_allow_ingress_from_quad_zero")
    try: 
        all_sg = get_security_groups()
        if not all_sg.security_groups: 
            logger.info("No Security-Groups found. Skipping Control compute_sg_allow_ingress_from_quad_zero...")
            return
        findings = []
        found_sg = []
        for sg in all_sg.security_groups:
            risky_rules = []
            for rule in sg.rules:
                if (rule.network == "0.0.0.0/0" or rule.network == "::0/0") and rule.flow_direction == "ingress":
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