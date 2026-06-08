import json
from datetime import date
import logging

logger = logging.getLogger(__name__) # use instead of print. can use print for developmemnt and debugging

def load_data():
    file_path = f"./data/YT_data_{date.today()}.json"

    try:
        logger.info(f"Processing file: YT_data_{date.today()}.json")

        with open(file_path, 'r', encoding='utf-8') as raw_data:
            data = json.load(raw_data) #this loads the whole json file into memory. if unlike now, the file is large, stream the json using a library like ijson to avoid performance issues

        return data
    
    except FileNotFoundError:
        logger.error(f'File not found: {file_path}')
        raise
    except json.JSONDecodeError:
        logger.error(f"Invalide JSON in file: {file_path}")
        raise