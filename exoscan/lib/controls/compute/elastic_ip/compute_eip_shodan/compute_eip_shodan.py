import sys, os, requests
from exoscan.lib.controls.compute.elastic_ip.inventory import get_elastic_ip
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_eip_shodan")

    api_key = os.getenv('SHODAN_API_KEY')
 
    if not api_key:
        logger.warning("SHODAN_API_KEY not set. Skipping control compute_eip_shodan...")
        return
    
    try: 
        all_eip = get_elastic_ip()
        if not all_eip.elastic_ips: 
            logger.info("No elastic IPs found. Skipping Control compute_eip_shodan...")
            return

        findings = []
        found_eips = []

        
        for eip in all_eip.elastic_ips:
            ip = eip.ip
            try:
                response = requests.get(f"https://api.shodan.io/shodan/host/{ip}?key={api_key}", timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    cves = set()

                    for service in data.get("data", []):
                        for cve in service.get("vulns", {}).keys():
                            cves.add(cve)

                    if cves:
                        cve_str = "\n    ".join(sorted(cves))
                        found_eips.append(f"{ip}:\n    {cve_str}")

                elif response.status_code == 404:
                    logger.debug(f"IP {ip} not found in Shodan.")
                else:
                    logger.warning(f"Shodan query failed for IP {ip}. Status code: {response.status_code}")

            except Exception as e:
                logger.error(f"Error querying Shodan for IP {ip}: {e}")

        if found_eips:
            eip_str = "\n - ".join(found_eips)
            findings.append(Finding.from_metadata(
                metadata_file=metadata_path,
                resource_description=f"Elastic IPs with known CVEs:\n - {eip_str}"
            ))

        return findings

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
    return