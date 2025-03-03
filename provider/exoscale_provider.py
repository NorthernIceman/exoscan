from log_conf.logger import logger 

def check_file_for_string(file_path, target_string="XXXXXX"):
    with open(file_path, "r", encoding="utf-8") as file:
        return target_string in file.read()

def authenticate():
    print("Hello from exoscale_provider.authenticate")

    file_path = "provider/credentials.txt" 
    if check_file_for_string(file_path):
        logger.info("No credentials supplied! Please submit them in provider/credentials.txt")
        return 
    else:
        print("ToDo")
        return 0


