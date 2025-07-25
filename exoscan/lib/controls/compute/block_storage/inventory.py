import requests, os, json, sys
from provider.exoscale_provider import authenticate
from exoscan.lib.controls.models import BlockStorageVolume, BlockStorageSnapshot, BlockStorageSnapshotContainer, BlockStorageVolumeContainer
from provider.return_regions import return_regions
from log_conf.logger import logger 

CACHE_FILE_VOLUME = "exoscan/lib/controls/compute/block_storage/block_storage_volume.inventory.json"
CACHE_FILE_SNAPSHOT = "exoscan/lib/controls/compute/block_storage/instance_snapshot.inventory.json"


def get_block_storage_volumes(
        volume_id: str = None
) -> BlockStorageVolumeContainer | BlockStorageVolume:
    try:
        if not os.path.exists(CACHE_FILE_VOLUME):
            logger.info("Volume cache not found. Creating full inventory...")
            regions = return_regions()
            auth = authenticate()

            all_volumes = []

            for region in regions:
                response = requests.get(f"https://api-{region}.exoscale.com/v2/block-storage", auth=auth)
                if response.status_code == 200:
                    for volume in response.json().get("block-storage-volumes", []):
                        print(f"{volume["id"]}")
                        details_response  = requests.get(f"https://api-{region}.exoscale.com/v2/block-storage/{volume["id"]}", auth=auth)
                        if details_response.status_code == 200:
                            all_volumes.append(details_response.json())
                            
            container = BlockStorageVolumeContainer.model_validate({"block-storage-volumes": all_volumes})

            with open(CACHE_FILE_VOLUME, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)

        with open(CACHE_FILE_VOLUME, "r") as f:
            json_data = json.load(f)

        if volume_id:
            for volume in json_data.get("block-storage-volumes", []):
                if volume.get("id") == volume_id:
                    return BlockStorageVolume.model_validate(volume)

            raise Exception(f"Volume ID '{volume_id}' not found in cached inventory.")

        return BlockStorageVolumeContainer.model_validate(json_data)

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)

def get_block_storage_snapshots(
        snapshot_id: str = None
) -> BlockStorageSnapshotContainer | BlockStorageSnapshot:
    try:
        if not os.path.exists(CACHE_FILE_VOLUME):
            logger.info("Snapshot cache not found. Creating full inventory...")
            regions = return_regions()
            auth = authenticate()

            all_snapshots = []

            for region in regions:
                response = requests.get(f"https://api-{region}.exoscale.com/v2/block-storage-snapshot", auth=auth)
                if response.status_code == 200:
                    for snapshot in response.json().get("block-storage-snapshots", []):
                        details_response  = requests.get(f"https://api-{region}.exoscale.com/v2/block-storage-snapshot/{snapshot["id"]}", auth=auth)
                        if details_response.status_code == 200:
                            all_snapshots.append(details_response.json())
                            
            container = BlockStorageSnapshotContainer.model_validate({"block-storage-snapshots": all_snapshots})

            with open(CACHE_FILE_VOLUME, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)

        with open(CACHE_FILE_VOLUME, "r") as f:
            json_data = json.load(f)

        if snapshot_id:
            for volume in json_data.get("block-storage-snapshots", []):
                if volume.get("id") == snapshot_id:
                    return BlockStorageSnapshot.model_validate(volume)

            raise Exception(f"Snapshot ID '{snapshot_id}' not found in cached inventory.")

        return BlockStorageSnapshotContainer.model_validate(json_data)

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
