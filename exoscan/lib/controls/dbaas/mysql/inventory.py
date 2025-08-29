import requests, os, json, sys, tempfile
from provider.exoscale_provider import authenticate
from exoscan.lib.controls.models import DBaaServiceMySQL, DBaaServiceMySQLContainer
from exoscan.lib.controls.dbaas.general.inventory import get_dbaas
from log_conf.logger import logger 

_temp_cache = tempfile.NamedTemporaryFile(
    prefix="mysql_inventory_", suffix=".json", delete=False
)
CACHE_FILE = _temp_cache.name

def get_dbaas_mysql() -> DBaaServiceMySQL | DBaaServiceMySQLContainer:
    try:
        if not os.path.exists(CACHE_FILE):
            logger.info("DBaaS cache not found. Creating full inventory...")
            all_mysql_dbs = get_dbaas("mysql")
            auth = authenticate()
            all_dbaas = []
            #API for DBaaS is different: need to get name of all types (pg, mysql, ...) then for details need own inventory with its own url. so here, we only get the service overview which serves other inventory files as name-type-inventory
            if not all_mysql_dbs: 
                logger.info("No MySQL-DBaaS found.")
                return
            for db in all_mysql_dbs:
                response = requests.get(f"https://api-{db['zone']}.exoscale.com/v2/dbaas-mysql/{db['name']}", auth=auth)
                if response.status_code == 200:
                    all_dbaas.append(response.json())

            container = DBaaServiceMySQLContainer.model_validate({"dbaas-mysql-services": all_dbaas})


            with open(CACHE_FILE, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)

        with open(CACHE_FILE, "r") as f:
            json_data = json.load(f)

        return DBaaServiceMySQLContainer.model_validate(json_data)

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
