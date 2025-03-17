import logging

def set_logging_config(verbose):
    formatter = logging.Formatter(
        "{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )

    logging_handlers = []

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    if verbose: console_handler.setLevel(10)
    else: console_handler.setLevel(30)
    
    file_handler = logging.FileHandler("exoscan.log", mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(10)

    logging_handlers.append(console_handler)
    logging_handlers.append(file_handler)

    logging.basicConfig(handlers=logging_handlers, level=logging.INFO)


logger = logging.getLogger()


