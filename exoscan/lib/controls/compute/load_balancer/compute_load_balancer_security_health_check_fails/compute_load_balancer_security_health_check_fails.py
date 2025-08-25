import sys
from exoscan.lib.controls.compute.load_balancer.inventory import get_load_balancer
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_load_balancer_security_health_check_fails")
    try: 
        all_lb = get_load_balancer()
        if not all_lb.load_balancers: 
            logger.info("No load-balancers found. Skipping Control compute_load_balancer_security_health_check_fails...")
            return

        findings = []
        found_lb = []
        found_services = []
        for lb in all_lb.load_balancers:
            if not lb.services: break
            for service in lb.services:
                 healthcheck_port = service.healthcheck.port
                 for healthcheck in service.healthcheck_status:
                    if healthcheck.status != "success":
                        found_services.append(service.name)
            if found_services:
                service_str = "\n    ".join(found_services)
                found_lb.append(f"{lb.name}:\n    {service_str}")        
                     
        if found_lb:
                lb_str = "\n - ".join(found_lb)
                findings.append(Finding.from_metadata(
                    metadata_file= metadata_path,
                    resource_description=f"Load-Balancers: \n - {str(lb_str)}"
                ))
                return findings

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return