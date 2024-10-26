from tqdm import tqdm
import concurrent.futures
import csv

from listings import ListingsProcessor
from common_setup import *

setup_logger("property_listings")

listings_folder = os.path.join('logs', 'listings')
os.makedirs(listings_folder, exist_ok=True)

POSTCODE_ERROR_TXT = os.path.join(listings_folder, 'postcode_error_property_listings.txt')
POSTCODE_SUCCESS_TXT = os.path.join(listings_folder, 'postcode_success_property_listings.txt')
LISTINGID_ERROR_TXT = os.path.join(listings_folder, 'listingid_error_property_listings.txt')

def process_property_listings(postcode):
    listings_processor = ListingsProcessor(logger)

    new_listing_ids = set()
    existing_listing_ids = load_listing_main_ids()

    try:
        listings = listings_processor.fetch_listing(postcode)
        if not listings:
            logger.warning(f"No listings found for {postcode}")
            with open(POSTCODE_SUCCESS_TXT, 'a') as f:
                f.write(f"{postcode} - 0\n")
        else:
            def process_single_listing(listing):
                # print(f"Processing {postcode}...")
                listing_id = listing.get('listingId')
                new_listing_ids.add(listing_id) 
                if listing_id not in existing_listing_ids:                    
                    sold_status = 'No'  
                    listing_dict_to_be_pushed = {
                        'ref_postcode': postcode,
                        'soldStatus': sold_status
                    }
                    listing_dict_to_be_pushed.update(listing)

                    listing_details = listings_processor.fetch_listing_details(listing_id)
                    if listing_details:
                        listing_dict_to_be_pushed.update(listing_details)
                        listing_dict_to_be_pushed.pop('__typename', None)
                        listing_dict_to_be_pushed = convert_values_to_string(listing_dict_to_be_pushed)
                    else:
                        logger.error(f"Failed to get listing details for {listing_id}")
                        with open(LISTINGID_ERROR_TXT, 'a') as f:
                            f.write(f"{listing_id} - {postcode} - NO DETAILS\n")
                        listing_dict_to_be_pushed = convert_values_to_string(listing_dict_to_be_pushed)
                    
                    add_to_bulk('listings_main', listing_dict_to_be_pushed)

            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                futures = [executor.submit(process_single_listing, listing) for listing in listings]
                for future in concurrent.futures.as_completed(futures):
                    future.result()

            with open(POSTCODE_SUCCESS_TXT, 'a') as f:
                f.write(f"{postcode} - {len(listings)}\n")   

            # print("Processing sold listing ids...")

            sold_listing_ids = existing_listing_ids - new_listing_ids
            # print(f"Found {len(sold_listing_ids)} sold listings")

            BATCH_SIZE = 100
            sold_list = list(sold_listing_ids)
            
            for i in range(0, len(sold_list), BATCH_SIZE):
                
                batch = sold_list[i:i + BATCH_SIZE]
                # print(f"Processing batch of {len(batch)} sold listings ({i + 1} to {i + len(batch)} of {len(sold_list)})")
                
                for sold_id in batch:
                    try:
                        sold_listing_dict = {
                            'listingId': sold_id,
                            'ref_postcode': postcode,
                            'soldStatus': 'Yes'
                        }
                        # print(f"Adding sold listing {sold_id} to bulk...")
                        add_to_bulk('listings_main', sold_listing_dict)
                        # print(f"Successfully added sold listing {sold_id}")
                    except Exception as e:
                        # print(f"Error processing sold listing {sold_id}: {str(e)}")
                        logger.error(f"Error processing sold listing {sold_id}: {str(e)}")
                        # Continue processing other listings even if one fails
                        continue

            # print("Completed processing all sold listings")

            if not os.path.exists("listings_old.txt"):
                # print("listings_old.txt doesn't exist. Creating new file...")
                open("listings_old.txt", 'a').close()

            # print("About to open listings_old.txt...")
            try:
                with open("listings_old.txt", 'r') as f:
                    existing_lines = f.readlines()
                
                print(f"Read {len(existing_lines)} existing listings")
                
                # Filter out sold listings and write back
                updated_lines = []
                for line in existing_lines:
                    listing_id = line.strip()
                    if listing_id not in sold_listing_ids:
                        updated_lines.append(line)
                        # print(f"Keeping active listing: {listing_id}")
                
                # Write the filtered listings back
                # print(f"Writing {len(updated_lines)} active listings back to file...")
                with open("listings_old.txt", 'w') as f:
                    f.writelines(updated_lines)
                # print(f"Successfully wrote {len(updated_lines)} listings to file")

                # Add new listings to the file
                # print("Adding new listings to file...")
                with open("listings_old.txt", 'a') as f:
                    for listing_id in new_listing_ids:
                        f.write(f"{listing_id}\n")
                # print(f"Added {len(new_listing_ids)} new listings to file")

            except IOError as e:
                logger.error(f"Error handling listings file: {e}")
                raise

    except Exception as e:
        logger.error(f"Failed to process listings for {postcode}: {e}")
        with open(POSTCODE_ERROR_TXT, 'a') as f:
            f.write(f"{postcode}, listings, ERROR, {e}\n")


def main():
    create_index_if_not_exists('listings_main')
    csv_file_path = os.getenv("CSV_FILE_PATH")
    
    try:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            postcodes = [row[0] for row in reader]
            print(f"Processing {len(postcodes)} postcodes")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
            futures = {executor.submit(process_property_listings, postcode): postcode for postcode in postcodes}
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                try:
                    future.result()  
                except Exception as e:
                    logger.error(f"Error processing postcode {futures[future]}: {e}")
    
    except KeyboardInterrupt:
        logger.warning("Processing interrupted by user.")
        logger.info("Attempting to flush remaining records to Elasticsearch and saving to json...")
        final_bulk_flush()
        save_remaining_records_to_json()
        logger.info("Remaining records saved.")

    finally:
        logger.warning("Final bulk flush...")
        final_bulk_flush()
        logger.info("Listings processing complete.")
        print("Listings processing complete.")

if __name__ == "__main__":
    main()

