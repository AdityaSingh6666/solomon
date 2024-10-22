import json
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

def fetch_all_documents(index_name, save_interval=10):
    scroll_size = 10000
    scroll_time = '10m'
    response = es.search(
        index=index_name,
        body={'query': {'match_all': {}}}, 
        size=scroll_size,
        scroll=scroll_time
    )
    
    scroll_id = response['_scroll_id']
    hits = response['hits']['hits']
    scroll_count = 1
    
    while True:
        print(f"fetching document batch {scroll_count}")
        
        if scroll_count % save_interval == 0:
            save_json(hits, index_name)
        
        response = es.scroll(
            scroll_id=scroll_id,
            scroll=scroll_time
        )
        scroll_id = response['_scroll_id']
        new_hits = response['hits']['hits']
        
        if not new_hits:
            print(f"Finished fetching all documents from index '{index_name}'")
            break
        
        hits.extend(new_hits)
        scroll_count += 1
    
    es.clear_scroll(scroll_id=scroll_id)
    return hits

def save_json(hits, index_name):
    todays_date = datetime.now().strftime("%d-%m-%Y")
    folder_path = "./JSON"
    os.makedirs(folder_path, exist_ok=True)
    file_path = f"{folder_path}/{index_name}_{todays_date}.json"
    
    with open(file_path, "w") as file:
        json.dump([doc["_source"] for doc in hits], file, indent=4)
        print(f"Saved JSON data to '{file_path}'")

index_name = "rent_data"
all_documents = fetch_all_documents(index_name)

# Final save after all scrolls
save_json(all_documents, index_name)
time.sleep(60)

print(f"Backup of index '{index_name}' has been completed.")
