import requests, os, json, sys, tempfile
from provider.exoscale_provider import authenticate
from exoscan.lib.controls.models import SSHKeyContainer, SSHKey
from log_conf.logger import logger 

_temp_cache = tempfile.NamedTemporaryFile(
    prefix="ssh_keys_inventory_", suffix=".json", delete=False
)
CACHE_FILE = _temp_cache.name
#this function does not take any parameters, it returns all ssh-keys in the account; done on purpose, as api does not support detailed response
def get_ssh_keys() -> SSHKeyContainer | SSHKey:
      
    try:
        if not os.path.exists(CACHE_FILE) or os.path.getsize(CACHE_FILE) == 0:
            logger.info("Creating Inventory of ssh keys...")
            auth = authenticate()
            all_keys = []
            
            response = requests.get("https://api-at-vie-1.exoscale.com/v2/ssh-key", auth=auth)
            if response.status_code == 200:
                all_keys = response.json().get("ssh-keys", [])

            container = SSHKeyContainer.model_validate({"ssh-keys": all_keys})

            with open(CACHE_FILE, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)
            

        with open(CACHE_FILE, "r") as f:
            json_data = json.load(f)

        return SSHKeyContainer.model_validate(json_data)
    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)

    


