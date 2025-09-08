import requests, os, json, sys, tempfile
from provider.exoscale_provider import authenticate, return_regions
from exoscan.lib.controls.models import DBaaService, DBaaServiceContainer
from log_conf.logger import logger 

_temp_cache = tempfile.NamedTemporaryFile(
    prefix="dbaas_inventory_", suffix=".json", delete=False
)
CACHE_FILE = _temp_cache.name

def get_dbaas(
        dbaas_type: str = None
) -> DBaaServiceContainer | DBaaService:
    try:
        if not os.path.exists(CACHE_FILE) or os.path.getsize(CACHE_FILE) == 0:
            logger.info("DBaaS cache not found. Creating full inventory...")
            regions = return_regions()
            auth = authenticate()

            all_dbaas = []
            
            for region in regions:
                response = requests.get(f"https://api-{region}.exoscale.com/v2/dbaas-service", auth=auth)
                if response.status_code == 200 and response:
                    for dbaas in response.json().get("dbaas-services", []):
                        dbass_name = dbaas.get("name")
                        if dbass_name: all_dbaas.append(dbaas)

            container = DBaaServiceContainer.model_validate({"dbaas-services": all_dbaas})

            with open(CACHE_FILE, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)

        with open(CACHE_FILE, "r") as f:
            json_data = json.load(f)

        if dbaas_type:
            dbaas_dict = [] #a list for all names of db of this type, so they can be processed by detail-inventory functions
            for db in json_data.get("dbaas-services", []):
                if db.get("type") == dbaas_type:
                    dbaas_dict.append({"name": db.get("name"), "zone" : db.get("zone")})
            if dbaas_dict: 
                return dbaas_dict

            return

        return DBaaServiceContainer.model_validate(json_data)

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
