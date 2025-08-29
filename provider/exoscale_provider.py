import sys, os
from log_conf.logger import logger 
from exoscale_auth import ExoscaleV2Auth
import boto3
from botocore.client import Config

EXOSCALE_API_KEY = os.getenv('EXOSCALE_API_KEY')
EXOSCALE_API_SECRET = os.getenv('EXOSCALE_API_SECRET')

def authenticate(): #returns the authentication header after parsing the file content
    try:
        if EXOSCALE_API_KEY == None and EXOSCALE_API_SECRET == None: 
            raise ConnectionAbortedError
        else: 
            auth = ExoscaleV2Auth(EXOSCALE_API_KEY, EXOSCALE_API_SECRET)
            return auth
    except (ConnectionAbortedError):
        logger.error("Authentication Methods could not find credentials in the form of env vars.")
        sys.exit("Authentication impossible, exiting...")

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
    


