import requests, os, json, sys
from provider.exoscale_provider import authenticate, return_regions
from exoscan.lib.controls.models import PrivateNetwork, PrivateNetworkContainer
from log_conf.logger import logger 

CACHE_FILE = "exoscan/lib/controls/compute/private_networks/private_networks.inventory.json"

def get_private_networks(
        private_network_id: str = None
) -> PrivateNetworkContainer | PrivateNetwork:
    try:
        if not os.path.exists(CACHE_FILE):
            logger.info("PrivateNetwork cache not found. Creating full inventory...")
            regions = return_regions()
            auth = authenticate()

            all_pn = []

            for region in regions:
                response = requests.get(f"https://api-{region}.exoscale.com/v2/private-network", auth=auth)
                if response.status_code == 200:
                    for pn in response.json().get("private-networks", []):
                        details_response  = requests.get(f"https://api-{region}.exoscale.com/v2/private-network/{pn["id"]}", auth=auth)
                        if details_response.status_code == 200:
                            all_pn.append(details_response.json())

            container = PrivateNetworkContainer.model_validate({"private-networks": all_pn})

            with open(CACHE_FILE, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)

        # Load from cache now (it exists for sure)
        with open(CACHE_FILE, "r") as f:
            json_data = json.load(f)

        if private_network_id:
            for pn in json_data.get("private-networks", []):
                if pn.get("id") == private_network_id:
                    return PrivateNetwork.model_validate(pn)

            raise Exception(f"Private Network ID '{private_network_id}' not found in cached inventory.")

        return PrivateNetworkContainer.model_validate(json_data)

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
