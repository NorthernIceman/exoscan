import sys
from exoscan.lib.controls.storage.buckets.inventory import get_sos_buckets
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: storage_buckets_versioning_enabled")
    try: 
        all_buckets = get_sos_buckets()
        if not all_buckets.sos_buckets_usage: 
            logger.info("No buckets found. Skipping Control storage_bucketstorage_buckets_versioning_enableds_acl_full_control_AllUsers...")
            return

        findings = []
        found_buckets = []

        for bucket in all_buckets.sos_buckets_usage:
            if bucket.versioning != "Enabled":
                found_buckets.append(bucket.name)
        
        if found_buckets:
                buckets_str = "\n - ".join(set(found_buckets))
                findings.append(Finding.from_metadata(
                    metadata_file= metadata_path,
                    resource_description=f"Buckets: \n - {str(buckets_str)}"
                ))
        return findings

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return