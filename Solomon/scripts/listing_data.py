import json
from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch, helpers
import dotenv
import os
import warnings
import csv
import time
from datetime import datetime

warnings.filterwarnings("ignore")

dotenv.load_dotenv(override=True)

url = str(os.getenv("DB_URL"))
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")

# Single Elasticsearch connection
es = Elasticsearch(
    [url],
    basic_auth=(username, password),
    verify_certs=False,
    timeout=600
)

def fetch_all_documents(index_name):
    scroll_size = 10000
    scroll_time = '10m'
    response = es.search(
        index=index_name,
        body={'query': {'match_all': {}}},
        size=scroll_size,
        scroll=scroll_time
    )
    print("fetching a document")
    scroll_id = response['_scroll_id']
    hits = response['hits']['hits']
    i = 0
    while True:
        print(f"fetching a document {i}")
        response = es.scroll(
            scroll_id=scroll_id,
            scroll=scroll_time
        )
        scroll_id = response['_scroll_id']
        hits.extend(response['hits']['hits'])

        if not response['hits']['hits']:
            print(f"Finished fetching all documents from index '{index_name}'")
            break
        
        i += 1
    es.clear_scroll(scroll_id=scroll_id)
    return hits

index_name = "price_paid_new"
todays_date = datetime.now().strftime("%d-%m-%Y")

folder_path = "./JSON"
os.makedirs(folder_path, exist_ok=True)

file_path = f"{folder_path}/{index_name}_{todays_date}.json"


all_documents = fetch_all_documents(index_name)
all_documents = [doc["_source"] for doc in all_documents]

with open(file_path, "w") as file:
    json.dump(all_documents, file, indent=4)
    time.sleep(60)
    
print(f"Backup of index '{index_name}' has been saved to '{file_path}'")