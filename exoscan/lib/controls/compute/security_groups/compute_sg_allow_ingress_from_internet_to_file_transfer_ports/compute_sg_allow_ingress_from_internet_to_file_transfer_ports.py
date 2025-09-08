import sys
from exoscan.lib.controls.compute.security_groups.inventory import get_security_groups
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_sg_allow_ingress_from_internet_to_file_transfer_ports")
    try: 
        all_sg = get_security_groups()
        if not all_sg.security_groups: 
            logger.info("No Security-Groups found. Skipping Control compute_sg_allow_ingress_from_internet_to_file_transfer_ports...")
            return
        findings = []
        ports = [20, 21]
        found_sg = []
        for sg in all_sg.security_groups:
            found_rules = []
            if sg.rules:
                for rule in sg.rules:
                    if rule.network and rule.start_port and rule.end_port:
                        if rule.network in ["0.0.0.0/0", "::/0"] and rule.flow_direction == "ingress":
                            matched_ports = []
                            for port in ports:
                                if port in range(int(rule.start_port), int(rule.end_port) + 1):
                                    matched_ports.append(f"{port}/{rule.protocol}")
                            if matched_ports:
                                ports_str = ", ".join(sorted(matched_ports))
                                found_rules.append(f"(Rule-ID: {rule.id}, Ports: {ports_str})")
            if found_rules:
                rules_str = "\n    ".join(found_rules)
                found_sg.append(f" - Security-Group: {sg.name}\n    {rules_str}")
        if found_sg:
            sgs_str = "\n".join(found_sg)
            findings.append(Finding.from_metadata(
                    metadata_file=metadata_path,
                    resource_description=f"Security-Groups:\n{sgs_str}"
                ))
        return findings
                
    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return