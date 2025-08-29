import requests, os, json, sys, tempfile
from provider.exoscale_provider import authenticate, return_regions
from exoscan.lib.controls.models import LoadBalancer, LoadBalancerContainer
from log_conf.logger import logger 

_temp_cache = tempfile.NamedTemporaryFile(
    prefix="load_balancer_inventory_", suffix=".json", delete=False
)
CACHE_FILE = _temp_cache.name

def get_load_balancer(
        load_balancer_id: str = None
) -> LoadBalancerContainer | LoadBalancer:
    try:
        if not os.path.exists(CACHE_FILE) or os.path.getsize(CACHE_FILE) == 0:
            logger.info("LoadBalancer cache not found. Creating full inventory...")
            regions = return_regions()
            auth = authenticate()

            all_instance_pools = []

            for region in regions:
                response = requests.get(f"https://api-{region}.exoscale.com/v2/load-balancer", auth=auth)
                if response.status_code == 200:
                    for lb in response.json().get("load-balancers", []):
                        details_response  = requests.get(f"https://api-{region}.exoscale.com/v2/load-balancer/{lb["id"]}", auth=auth)
                        if details_response.status_code == 200:
                            all_instance_pools.append(details_response.json())

            container = LoadBalancerContainer.model_validate({"load-balancers": all_instance_pools})

            with open(CACHE_FILE, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)

        # Load from cache now (it exists for sure)
        with open(CACHE_FILE, "r") as f:
            json_data = json.load(f)

        if load_balancer_id:
            for lb in json_data.get("load-balancers", []):
                if lb.get("id") == load_balancer_id:
                    return LoadBalancer.model_validate(lb)

            raise Exception(f"LoadBalancer ID '{load_balancer_id}' not found in cached inventory.")

        return LoadBalancerContainer.model_validate(json_data)

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
