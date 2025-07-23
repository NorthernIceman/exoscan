import sys
from exoscan.lib.controls.compute.private_networks.inventory import get_private_networks
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_private_networks_leases_reach_threshold")
    try: 
        all_pn = get_private_networks()
        if not all_pn.private_networks: 
            logger.info("No private networks found. Skipping Control compute_private_networks_leases_reach_threshold...")
            return

        findings = []
        found_pn = []
        threshold = 80

        for pn in all_pn.private_networks:
            if not pn.netmask: break   
            number_of_ips = 2 ** (32 - (sum([bin(int(x)).count("1") for x in pn.netmask.split(".")]))) - 2 #calculate how many ips are in the subnet (- networkaddress and broadcastaddress)
            number_of_leases = len(pn.leases) if pn.leases else 0
            capacity = 100 / number_of_ips * number_of_leases
            if capacity >= threshold:
                found_pn.append(f"{pn.name}: {capacity:.2f}%")

                     
        if found_pn:
                pn_str = "\n - ".join(found_pn)
                findings.append(Finding.from_metadata(
                    metadata_file= metadata_path,
                    resource_description=f"Private-Networks: \n - {str(pn_str)}"
                ))
                return findings

    except Exception as error:
        logger.error(f"1{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return