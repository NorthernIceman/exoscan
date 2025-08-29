import requests, os, json, sys, tempfile
from provider.exoscale_provider import authenticate, get_s3_client
from exoscan.lib.controls.models import SOSBucket, SOSBucketContainer
from log_conf.logger import logger 

_temp_cache = tempfile.NamedTemporaryFile(
    prefix="sos_buckets_inventory_", suffix=".json", delete=False
)
CACHE_FILE = _temp_cache.name

def get_sos_buckets() -> SOSBucketContainer | SOSBucket:
      
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                json_data = json.load(f)
        else:
            logger.info("Creating Inventory of sos-buckets-usage...")
            auth = authenticate()
            all_buckets = []
            
            # Only need one region for this API call
            response = requests.get("https://api-at-vie-1.exoscale.com/v2/sos-buckets-usage", auth=auth).json()
            all_buckets = response.get("sos-buckets-usage", [])
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
            
            json_data = {"sos-buckets-usage": all_buckets}
            container = SOSBucketContainer.model_validate(json_data)

            with open(CACHE_FILE, "w") as f:
                json.dump(container.model_dump(by_alias=True), f, indent=2)
            return container
        return SOSBucketContainer.model_validate(json_data)
    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)

    


