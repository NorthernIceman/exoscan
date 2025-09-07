import sys
from exoscan.lib.controls.compute.load_balancer.inventory import get_load_balancer
from exoscan.lib.controls.compute.instance_pools.inventory import get_instance_pools
from exoscan.lib.controls.compute.security_groups.inventory import get_security_groups
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_load_balancer_security_group_blocks_health_check")
    try: 
        all_lb = get_load_balancer()
        if not all_lb.load_balancers: 
            logger.info("No load-balancers found. Skipping Control compute_load_balancer_security_group_blocks_health_check...")
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
                        print("A")
                        instance_pool = get_instance_pools(service.instance_pool.id)
                        security_groups = instance_pool.security_groups
                        for sg in security_groups:
                            print("B")
                            security_group_details = get_security_groups(sg.id)
                            for rule in security_group_details.rules:
                                print(healthcheck_port, rule.start_port, rule.end_port)
                                if healthcheck_port not in range(rule.start_port, rule.end_port + 1):
                                    print("c")
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