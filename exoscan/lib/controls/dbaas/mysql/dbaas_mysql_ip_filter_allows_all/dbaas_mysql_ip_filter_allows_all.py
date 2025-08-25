import sys
from exoscan.lib.controls.dbaas.mysql.inventory import get_dbaas_mysql
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: dbaas_mysql_ip_filter_allows_all")
    try: 
        all_mysql_dbaas = get_dbaas_mysql()
        if not all_mysql_dbaas: 
            logger.info("No MySQL-DBaaS found. Skipping Control dbaas_mysql_ip_filter_allows_all...")
            return
        findings = []
        found_dbs = []

        for db in all_mysql_dbaas.dbaas_mysql_services:
            if db.ip_filter and "0.0.0.0/0" in db.ip_filter:
                found_dbs.append(db.name)
  
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