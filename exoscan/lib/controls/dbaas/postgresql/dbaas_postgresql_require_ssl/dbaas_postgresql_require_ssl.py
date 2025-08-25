import sys
from exoscan.lib.controls.dbaas.postgresql.inventory import get_dbaas_pg
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: dbaas_postgresql_require_ssl")
    try: 
        all_pg_dbaas = get_dbaas_pg()
        if not all_pg_dbaas: 
            logger.info("No PostgreSQL-DBaaS found. Skipping Control dbaas_postgresql_require_ssl...")
            return
        findings = []
        found_dbs = []

        for db in all_pg_dbaas.dbaas_pg_services:
            if db.uri_params.sslmode and db.uri_params.sslmode != "require": #invert logic
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