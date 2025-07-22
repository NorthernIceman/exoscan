import requests, os, json, sys
from provider.exoscale_provider import authenticate
from exoscan.lib.controls.models import SKSClusterContainer, SKSCluster
from provider.return_regions import return_regions
from log_conf.logger import logger 

#here shall be functions to build an inventory, iterate through all regions and list the cluster. 
#to save api-calls, a file is created the first time a request is made
#TODO: cleanup all inventory files after program is done

CACHE_FILE = "exoscan/lib/controls/compute/sks/sks.inventory.json"

def get_sks(
        sks_id: str = None
) -> SKSClusterContainer | SKSCluster:
    try:
        if not os.path.exists(CACHE_FILE):
            logger.info("SKS cache not found. Creating full inventory...")
            regions = return_regions()
            auth = authenticate()

            all_sks_cluster = []

            for region in regions:
                response = requests.get(f"https://api-{region}.exoscale.com/v2/sks-cluster", auth=auth)
                if response.status_code == 200:
                    for cluster in response.json().get("sks-clusters", []):
                        details_response  = requests.get(f"https://api-{region}.exoscale.com/v2/sks-cluster/{cluster["id"]}", auth=auth)
                        if details_response.status_code == 200:
                            cluster_details = details_response.json()
                            all_sks_cluster.append(cluster_details)

            container = SKSClusterContainer.model_validate({"sks-clusters": all_sks_cluster})

            with open(CACHE_FILE, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)

        # Load from cache now (it exists for sure)
        with open(CACHE_FILE, "r") as f:
            json_data = json.load(f)

        if sks_id:
            for cluster in json_data.get("sks-clusters", []):
                if cluster.get("id") == sks_id:
                    return SKSCluster.model_validate(cluster)

            raise Exception(f"Cluster ID '{sks_id}' not found in cached inventory.")

        return SKSClusterContainer.model_validate(json_data)

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)

def get_sks_versions():
    try: 
        auth = authenticate()
        url = f"https://api-at-vie-2.exoscale.com/v2/sks-cluster-version"
        available_versions = requests.get(url, auth=auth).json()
        return available_versions['sks-cluster-versions']

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)