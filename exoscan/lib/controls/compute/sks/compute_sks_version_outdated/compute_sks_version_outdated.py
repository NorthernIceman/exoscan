import sys, requests
from exoscan.lib.controls.compute.sks.inventory import get_sks, get_sks_versions
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: compute_sks_version_outdated")
    try: 
        all_cluster = get_sks()
        if not all_cluster.sks_cluster: 
            logger.info("No sks-cluster found. Skipping Control compute_sks_version_outdated...")
            return

        findings = []
        found_cluster = []

        available_versions = get_sks_versions()
        for cluster in all_cluster.sks_cluster:
            if cluster.version and cluster.version not in available_versions:
                 
                 found_cluster.append(cluster.name)
        if found_cluster:
                cluster_str = "\n - ".join(found_cluster)
                findings.append(Finding.from_metadata(
                    metadata_file= metadata_path,
                    resource_description=f"SKS-Cluster: \n - {str(cluster_str)}"
                ))
        return findings

    except Exception as error:
        logger.error(f"1{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return