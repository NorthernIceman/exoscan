import sys
from exoscan.lib.controls.dbaas.general.inventory import get_dbaas
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: dbaas_general_termination_protection_off")
    try: 
        all_dbaas = get_dbaas()
        if not all_dbaas: 
            logger.info("No DBaaS found. Skipping Control dbaas_general_termination_protection_off...")
            return
        findings = []
        found_dbs = []

        for db in all_dbaas.dbaas_services:
            if db.termination_protection != True:
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