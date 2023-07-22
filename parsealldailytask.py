from pymongo import MongoClient
from libs.parser_1.other_module import parser_solo
import datetime
import time

# Connect to MongoDB
client = MongoClient('mongodb+srv://user_yarpshe:Q1w2e3r4_0@cluster0.aktya2j.mongodb.net/')
db = client['test_1506']
collection = db['test']

def parse_all_urls():
    # Retrieve all documents from the collection
    documents = collection.find()
    total_urls = collection.count_documents({})

    # Initialize counters
    parsed_urls = 0
    errors = 0

    # Loop through each document and parse the URL
    for document in documents:
        url = document['Link']

        try:
            # Perform parsing using the parse_solo function
            parsed_data = parser_solo(url)

            # Update the document in MongoDB with the parsed data
            collection.update_one(
                {'_id': document['_id']},
                {'$set': {'Price': parsed_data[0], 'Stock': parsed_data[1]}}
            )

            parsed_urls += 1
        except Exception as e:
            print(f"Error parsing URL: {url}")
            print(f"Error message: {str(e)}")
            errors += 1

    # Print summary
    print(f"Total URLs: {total_urls}")
    print(f"Parsed URLs: {parsed_urls}")
    print(f"Errors: {errors}")

# Schedule the parsing task to run daily at 9 a.m. New York time
if __name__ == '__main__':
    while True:
        now = datetime.datetime.now()
        if now.hour == 2 and now.minute == 7:
            parse_all_urls()
        time.sleep(60)  # Sleep for 1 minute before checking the time again

