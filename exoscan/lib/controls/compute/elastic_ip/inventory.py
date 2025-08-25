import requests, os, json, sys
from provider.exoscale_provider import authenticate, return_regions
from exoscan.lib.controls.models import ElasticIP, ElasticIPContainer
from log_conf.logger import logger 

CACHE_FILE = "exoscan/lib/controls/compute/elastic_ip/elastic_ip.inventory.json"

def get_elastic_ip(
        elastic_ip_id: str = None
) -> ElasticIPContainer | ElasticIP:
    try:
        if not os.path.exists(CACHE_FILE):
            logger.info("Elastic-IP cache not found. Creating full inventory...")
            regions = return_regions()
            auth = authenticate()

            all_eips = []

            for region in regions:
                response = requests.get(f"https://api-{region}.exoscale.com/v2/elastic-ip", auth=auth)
                if response.status_code == 200:
                    for eip in response.json().get("elastic-ips", []):
                        details_response  = requests.get(f"https://api-{region}.exoscale.com/v2/elastic-ip/{eip["id"]}", auth=auth)
                        if details_response.status_code == 200:
                            eip_details = details_response.json()
                            all_eips.append(eip_details)

            container = ElasticIPContainer.model_validate({"elastic-ips": all_eips})

            with open(CACHE_FILE, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)

        with open(CACHE_FILE, "r") as f:
            json_data = json.load(f)

        if elastic_ip_id:
            for eip in json_data.get("elastic-ips", []):
                if eip.get("id") == elastic_ip_id:
                    return ElasticIP.model_validate(eip)

            raise Exception(f"Elastic IP ID '{elastic_ip_id}' not found in cached inventory.")

        return ElasticIPContainer.model_validate(json_data)

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
