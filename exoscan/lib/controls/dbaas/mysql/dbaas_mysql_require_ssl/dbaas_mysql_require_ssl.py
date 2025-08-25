import sys
from exoscan.lib.controls.dbaas.mysql.inventory import get_dbaas_mysql
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: dbaas_mysql_require_ssl")
    try: 
        all_mysql_dbaas = get_dbaas_mysql()
        if not all_mysql_dbaas: 
            logger.info("No PostgreSQL-DBaaS found. Skipping Control dbaas_mysql_require_ssl...")
            return
        findings = []
        found_dbs = []

        for db in all_mysql_dbaas.dbaas_mysql_services:
            if hasattr(db.connection_info, "params"): #must search in connection info, as it is null in uri. different than postgresql
                for param in db.connection_info.params or []:
                    if param.get("ssl-mode", "").upper() != "REQUIRED":
                        found_dbs.append(db.name)
                        break
  
        if found_dbs:
            dbaas_str = "\n - ".join(set(found_dbs))
            findings.append(Finding.from_metadata(
                        metadata_file= metadata_path,
                        resource_description=f"DBaaS:\n - {dbaas_str}" #set to remove duplicates
                    ))
        return findings
                
    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return