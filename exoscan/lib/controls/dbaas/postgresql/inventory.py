import requests, os, json, sys, tempfile
from provider.exoscale_provider import authenticate
from exoscan.lib.controls.models import DBaaServicePostgreSQL, DBaaServicePostgreSQLContainer
from exoscan.lib.controls.dbaas.general.inventory import get_dbaas
from log_conf.logger import logger 

_temp_cache = tempfile.NamedTemporaryFile(
    prefix="postgresql_inventory_", suffix=".json", delete=False
)
CACHE_FILE = _temp_cache.name

def get_dbaas_pg() -> DBaaServicePostgreSQL | DBaaServicePostgreSQLContainer:
    try:
        if not os.path.exists(CACHE_FILE) or os.path.getsize(CACHE_FILE) == 0:
            logger.info("DBaaS cache not found. Creating full inventory...")
            all_pg_dbs = get_dbaas("pg")
            auth = authenticate()

            all_dbaas = []
            if not all_pg_dbs: 
                logger.info("No postgreSQL-DBaaS found.")
                return
            for db in all_pg_dbs:
                response = requests.get(f"https://api-{db['zone']}.exoscale.com/v2/dbaas-postgres/{db['name']}", auth=auth)
                if response.status_code == 200:
                    all_dbaas.append(response.json())

            container = DBaaServicePostgreSQLContainer.model_validate({"dbaas-pg-services": all_dbaas})


            with open(CACHE_FILE, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)

        with open(CACHE_FILE, "r") as f:
            json_data = json.load(f)

        return DBaaServicePostgreSQLContainer.model_validate(json_data)

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
