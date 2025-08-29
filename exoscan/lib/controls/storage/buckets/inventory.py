import requests, os, json, sys, tempfile
from provider.exoscale_provider import authenticate, get_s3_client
from exoscan.lib.controls.models import SOSBucket, SOSBucketContainer
from log_conf.logger import logger 

_temp_cache = tempfile.NamedTemporaryFile(
    prefix="sos_buckets_inventory_", suffix=".json", delete=False
)
CACHE_FILE = _temp_cache.name

#not necessary to take parameters
def get_sos_buckets() -> SOSBucketContainer | SOSBucket:
    try:
        if not os.path.exists(CACHE_FILE) or os.path.getsize(CACHE_FILE) == 0:
            logger.info("Creating Inventory of sos-buckets-usage...")
            auth = authenticate()
            all_buckets = []
            
            # Only need one region for this API call, because all buckets are returned
            response = requests.get("https://api-at-vie-1.exoscale.com/v2/sos-buckets-usage", auth=auth)
            if response.status_code == 200:
                all_buckets = response.json().get("sos-buckets-usage", [])
                for bucket in all_buckets: 
                    bucket_name = bucket.get("name")
                    region = bucket.get("zone-name")
                    if bucket_name and region:
                        s3_client = get_s3_client(region)
                        try:
                            acl_response = s3_client.get_bucket_acl(Bucket=bucket_name)
                            # Parse ACLs
                            bucket["ACL"] = acl_response.get("Grants", [])
                            cors_response = s3_client.get_bucket_cors(Bucket=bucket_name)
                            bucket["CORSRules"] = cors_response.get('CORSRules',[])
                            versioning_response = s3_client.get_bucket_versioning(Bucket=bucket_name)
                            bucket["Status"] = versioning_response.get('Status')
                        except Exception as acl_error:
                            logger.error(f"ACL fetch failed for bucket {bucket_name}: {acl_error}")
                            bucket["ACL"] = []
            
            container = SOSBucketContainer.model_validate({"sos-buckets-usage": all_buckets})

            with open(CACHE_FILE, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)

        with open(CACHE_FILE, "r") as f:
            json_data = json.load(f)

        return SOSBucketContainer.model_validate(json_data)

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)

    


