import sys
from log_conf.logger import logger 
from exoscale_auth import ExoscaleV2Auth
import requests

def authenticate(): #returns the authentication header after parsing the file content
    file_path = "provider/credentials.txt" 
    try:
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
            response = requests.get("https://api-ch-gva-2.exoscale.com/v2/", auth=auth)  #requests must iterate through every region
            
            return auth
    except (FileExistsError, FileNotFoundError):
        logger.error("File could not be opened or does not exist.")
        sys.exit("Authentication file not found. Abort...")


    


