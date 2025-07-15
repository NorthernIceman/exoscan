import requests, os, json, sys
from provider.exoscale_provider import authenticate
from exoscan.lib.controls.models import SSHKeyContainer, SSHKey
from log_conf.logger import logger 

#here shall be functions to build an inventory, iterate through all regions and list the ssh_keys. 
#to save api-calls, a file is created the first time a request is made
#TODO: cleanup all inventory files after program is done

CACHE_FILE = "exoscan/lib/controls/compute/ssh_keys/ssh_keys.inventory.json"

def get_ssh_keys() -> SSHKeyContainer | SSHKey:
      
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                json_data = json.load(f)
        else:
            logger.info("Creating Inventory of ssh-keys...")
            auth = authenticate()
            all_keys = []

            # Only need one region for this API call
            response = requests.get(
                "https://api-at-vie-1.exoscale.com/v2/ssh-key", auth=auth
            ).json()

            # Extract keys from response
            all_keys = response.get("ssh-keys", [])
            json_data = {"ssh-keys": all_keys}

            container = SSHKeyContainer.model_validate(json_data)

            with open(CACHE_FILE, "w") as f:
                json.dump(container.model_dump(by_alias=True), f, indent=2)
            return container
        return SSHKeyContainer.model_validate(json_data)
    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)

    


