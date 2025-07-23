import requests, os, json, sys
from provider.exoscale_provider import authenticate
from exoscan.lib.controls.models import InstancePool, InstancePoolContainer
from provider.return_regions import return_regions
from log_conf.logger import logger 

#here shall be functions to build an inventory, iterate through all regions and list the instances. 
#to save api-calls, a file is created the first time a request is made
#TODO: cleanup all inventory files after program is done

CACHE_FILE = "exoscan/lib/controls/compute/instance_pools/instance_pool.inventory.json"

def get_instance_pools(
        instance_pool_id: str = None
) -> InstancePoolContainer | InstancePool:
    try:
        if not os.path.exists(CACHE_FILE):
            logger.info("InstancePool cache not found. Creating full inventory...")
            regions = return_regions()
            auth = authenticate()

            all_instance_pools = []

            for region in regions:
                response = requests.get(f"https://api-{region}.exoscale.com/v2/instance-pool", auth=auth)
                if response.status_code == 200:
                    for instance_pool in response.json().get("instance-pools", []):
                        details_response  = requests.get(f"https://api-{region}.exoscale.com/v2/instance-pool/{instance_pool["id"]}", auth=auth)
                        if details_response.status_code == 200:
                            instance_pool_details = details_response.json()
                            all_instance_pools.append(instance_pool_details)

            container = InstancePoolContainer.model_validate({"instance-pools": all_instance_pools})

            with open(CACHE_FILE, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)

        # Load from cache now (it exists for sure)
        with open(CACHE_FILE, "r") as f:
            json_data = json.load(f)

        if instance_pool_id:
            for instance_pool in json_data.get("instance-pools", []):
                if instance_pool.get("id") == instance_pool_id:
                    return InstancePool.model_validate(instance_pool)

            raise Exception(f"Instance-Pool ID '{instance_pool_id}' not found in cached inventory.")

        return InstancePoolContainer.model_validate(json_data)

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
