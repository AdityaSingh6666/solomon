import os
import dotenv
from elasticsearch import Elasticsearch, helpers
from loguru import logger
import warnings
import threading
import traceback
import json
import random
from time import sleep

# Remove SSL warnings related to DB connection
warnings.filterwarnings("ignore")

dotenv.load_dotenv(override=True)

# Error folder setup
error_folder = 'errors'
if not os.path.exists(error_folder):
    os.makedirs(error_folder)

POSTCODE_ERROR_TXT = os.path.join(error_folder, 'postcode_errors.txt')
LISTINGID_ERROR_TXT = os.path.join(error_folder, 'listingid_errors.txt')
UPRN_ERROR_TXT = os.path.join(error_folder, 'uprn_errors.txt')
AGENTID_ERROR_TXT = os.path.join(error_folder, 'agentid_errors.txt')
BULK_PUSH_ERROR_TXT = os.path.join(error_folder, 'bulk_push_errors.txt')

# Create error txt files
for txt_file in [POSTCODE_ERROR_TXT, LISTINGID_ERROR_TXT, UPRN_ERROR_TXT, AGENTID_ERROR_TXT, BULK_PUSH_ERROR_TXT]:
    with open(txt_file, 'w') as f:
        f.write("Error\n")

# Thread lock for bulk operations
bulk_lock = threading.Lock()

# Elasticsearch setup
URL = os.getenv("DB_URL")
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")

es = Elasticsearch(
    [URL],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False,
    timeout=300
)

# Bulk insertion buffers
bulk_buffers = {
    'postcodes': [],
    'listings_main': [],
    'housing_prices_2': [],
    'agents_list': [],
    'walkscore': [],
    'walkscore_new': [],
}

BULK_SIZE = int(os.getenv("BULK_SIZE"))

def setup_logger(log_filename):
    # Create logs folder for easy access to progress
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    # Set up logger
    logger.remove()  # Remove the default logger
    logger.add(f"logs/{log_filename}.log", rotation="10 MB")

def create_index_if_not_exists(index_name):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
        logger.info(f"Index {index_name} created")
    else:
        logger.info(f"Index {index_name} already exists")

def convert_values_to_string(data):
    if data is None:
        return None
    elif isinstance(data, dict):
        return {k: convert_values_to_string(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_values_to_string(item) for item in data]
    else:
        return str(data)

def save_remaining_records_to_json():
    remaining_records = {index: docs for index, docs in bulk_buffers.items() if docs}
    if remaining_records:
        with open('remaining_records.json', 'w') as f:
            json.dump(remaining_records, f, indent=4)
        logger.info(f"Remaining records saved to remaining_records.json")

def add_to_bulk(index, document):
    bulk_buffers[index].append({
        '_index': index,
        '_source': document
    })
    
    with bulk_lock:
        if len(bulk_buffers[index]) >= BULK_SIZE:
            flush_bulk(index)

def flush_bulk(index_name):
    if bulk_buffers[index_name]:
        try:
            helpers.bulk(es, bulk_buffers[index_name], index=index_name)
            logger.info(f"Flushed {len(bulk_buffers[index_name])} documents to {index_name}")
            bulk_buffers[index_name].clear()
            sleep(15)
        except helpers.BulkIndexError as e:
            logger.error(f"(Indexing Error) Failed to flush bulk for {index_name}: {e}")
            logger.error(traceback.format_exc())

            failed_docs = set()
            for error in e.errors:
                if 'data' in error['index'] and 'listingId' in error['index']['data']:
                    failed_docs.add(error['index']['data']['listingId'])

            success_docs = [doc for doc in bulk_buffers[index_name] if doc['listingId'] not in failed_docs]

            with open(BULK_PUSH_ERROR_TXT, 'a') as f:
                for error in e.errors:
                    f.write(f"{index_name} - {error}\n")
            
            if success_docs:
                # Retry successful docs
                try:
                    helpers.bulk(es, success_docs, index=index_name)
                    logger.info(f"Successfully re-flushed {len(success_docs)} documents to {index_name}")
                except Exception as e:
                    logger.error(f"Failed to flush retry documents for {index_name}: {e}")
                    logger.error(traceback.format_exc())
                    with open(BULK_PUSH_ERROR_TXT, 'a') as f:
                        f.write(f"{index_name} - {traceback.format_exc()}\n")
            
            bulk_buffers[index_name].clear()
            
        except Exception as e:
            logger.error(f"Failed to flush bulk for {index_name}: {e}")
            logger.error(traceback.format_exc())
            with open(BULK_PUSH_ERROR_TXT, 'a') as f:
                f.write(f"{index_name} - {traceback.format_exc()}\n")

def final_bulk_flush():
    for index in bulk_buffers:
        # print(f"{index}: {len(bulk_buffers[index])}")
        if index:
            # print(f"Flushing {len(bulk_buffers[index])} documents for {index}")
            with bulk_lock:
                flush_bulk(index)
                save_remaining_records_to_json()
            # sleep(60)
        else:
            logger.info(f"No documents to flush for {index}")

def load_listing_main_ids():
    try:
        with open("listings_old.txt", 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()
