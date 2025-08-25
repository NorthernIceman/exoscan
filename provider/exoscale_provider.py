import sys, os
from log_conf.logger import logger 
from exoscale_auth import ExoscaleV2Auth
import boto3
from botocore.client import Config

EXOSCALE_API_KEY = os.getenv('EXOSCALE_API_KEY')
EXOSCALE_API_SECRET = os.getenv('EXOSCALE_API_SECRET')

def authenticate(): #returns the authentication header after parsing the file content
    file_path = "provider/credentials.txt" 
    try:
        if EXOSCALE_API_KEY == None and EXOSCALE_API_SECRET == None: 
            file = open(file_path, "r")
            api_key_line = file.readline()
            api_secret_line = file.readline()
            if ("XXXXXX" in (api_key_line or api_secret_line)):
                logger.info("No credentials supplied! Please submit them in provider/credentials.txt")
                sys.exit(1)
            else:
                API_KEY = api_key_line.split("=")[1].strip().strip('"').strip("'")
                API_SECRET = api_secret_line.split("=")[1].strip().strip('"').strip("'")
                auth = ExoscaleV2Auth(API_KEY, API_SECRET)
                return auth
        else: 
            auth = ExoscaleV2Auth(EXOSCALE_API_KEY, EXOSCALE_API_SECRET)
            return auth
                
    except (FileExistsError, FileNotFoundError):
        logger.error("File could not be opened or does not exist.")
        sys.exit("Authentication file not found. Abort...")

def get_s3_client(zone):
    endpoint = f'https://sos-{zone}.exo.io'
    try: 
        s3 = boto3.client(
                's3',
                endpoint_url=endpoint,
                aws_access_key_id=EXOSCALE_API_KEY,
                aws_secret_access_key=EXOSCALE_API_SECRET,
                config=Config(signature_version='s3v4'),
                region_name=zone
            )
        return s3
    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        return

def return_regions() -> list:
    return ("at-vie-1", "at-vie-2", "bg-sof-1", "ch-gva-2", "ch-dk-2", "de-fra-1", "de-muc-1", "hr-zag-1" )
    


