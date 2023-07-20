from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
from pymongo import MongoClient, UpdateOne
from bson.objectid import ObjectId
from libs.parser_1.other_module import parser_solo,count
import os
import traceback
import time
import pandas as pd
from math import ceil

# import pymongo
# import libraryparse
app = Flask(__name__)
socketio = SocketIO(app)
 

client = MongoClient('mongodb+srv://user_yarpshe:Q1w2e3r4_0@cluster0.aktya2j.mongodb.net/')
db = client['test_1506']
collection = db['test']

@app.route('/', defaults={'page_num': 1})
@app.route('/page/<int:page_num>', methods=['GET'])
def index(page_num):
    urls_per_page = 50
    skip_rows = (page_num - 1) * urls_per_page

    # Fetch URLs from the MongoDB collection based on pagination
    total_urls = collection.count_documents({})
    total_pages = ceil(total_urls / urls_per_page)

    # Get URLs for the current page
    urls = collection.find().skip(skip_rows).limit(urls_per_page)

    return render_template('index.html', urls=urls, current_page=page_num, total_pages=total_pages)

@app.route('/delete', methods=['POST'])
def delete_url():
    url_id = request.json.get('url_id')
    collection.delete_one({'_id': ObjectId(url_id)})
    return jsonify({'message': 'URL deleted successfully'})

@app.route('/addNewItem', methods=['POST'])
def add_new_item():
    sku = request.form.get('sku')
    link = request.form.get('url')
    price = 0
    stock = 'Out'

    new_item = {
        'SKU': sku,
        'Link': link,
        'Price': price,
        'Stock': stock
    }

    # Insert the new item into the collection
    collection.insert_one(new_item)

    # Redirect to the homepage to update the table
    return redirect('/')

# Add a route to handle the pagination request
@app.route('/page/<int:page_num>', methods=['GET'])
def pagination(page_num):
    urls_per_page = 50
    skip_rows = (page_num - 1) * urls_per_page

    # Fetch URLs from the MongoDB collection based on pagination
    total_urls = collection.count_documents({})
    total_pages = ceil(total_urls / urls_per_page)

    # Get URLs for the current page
    urls = collection.find().skip(skip_rows).limit(urls_per_page)

    return render_template('index.html', urls=urls, current_page=page_num, total_pages=total_pages)


@app.route('/add_multiple', methods=['POST'])
def add_multiple():
    if 'csv_file' not in request.files:
        return jsonify({'message': 'No CSV file provided.'}), 400

    file = request.files['csv_file']

    if file.filename == '':
        return jsonify({'message': 'No file selected.'}), 400

    if file and file.filename.endswith('.csv'):
        # Read the CSV file using pandas
        df = pd.read_csv(file)
        items_added = 0

        for index, row in df.iterrows():
            sku = row.get('SKU')
            link = row.get('Link')
            price = 0
            stock = 'Out'

            new_item = {
                'SKU': sku,
                'Link': link,
                'Price': price,
                'Stock': stock
            }

            # Insert the new item into the collection
            collection.insert_one(new_item)
            items_added += 1

        return jsonify({'message': f'{items_added} items added successfully.'})

    return jsonify({'message': 'Invalid file format. Only CSV files are allowed.'}), 400

@app.route('/parse_one', methods=['POST'])
def parse_one():
    # Get the URL ID from the request
    url_id = request.json.get('url_id')
    
    # Retrieve the URL from MongoDB based on the ID
    client = MongoClient('mongodb+srv://user_yarpshe:Q1w2e3r4_0@cluster0.aktya2j.mongodb.net/')
    db = client['test_1506']
    collection = db['test']
    
    # Find the document with the given ID
    document = collection.find_one({'_id': ObjectId(url_id)})
    
    if document:
        url = document['Link']
        # Perform parsing using the parse_solo function
        parsed_data = parser_solo(url)
        
        # Update the document in MongoDB with the parsed data
        collection.update_one(
            {'_id': ObjectId(url_id)},
            {'$set': {'Price': parsed_data[0], 'Stock': parsed_data[1]}}
        )
            
        return  """
        <script>
            alert('URL parsed successfully.');
            window.location.reload();
        </script>
        """
    
    return  jsonify({'message': 'URL not found.'}), 404
    
@app.route('/parse', methods=['POST'])
def parse_urls():
    try:
        # Get all the URLs from MongoDB
        urls = collection.find()

        # Calculate the total number of URLs to parse
        total_urls = count()

        # Start parsing and emit progress updates
        progress = 0
        for index, url in enumerate(urls):
            url_id = str(url['_id'])
            link = url['Link']
            parsed_urls = 0

            # Perform parsing using the parser_solo function
            parsed_data = parser_solo(link)

            # Update the document in MongoDB with the parsed data
            collection.update_one(
                {'_id': ObjectId(url_id)},
                {'$set': {'Price': parsed_data[0], 'Stock': parsed_data[1]}}
            )

            # Calculate progress and emit progress update
            parsed_urls += 1
            progress = int((index + 1) / total_urls * 100)
            socketio.emit('progress_update', {'progress': progress}, namespace='/')
            socketio.sleep(0.5)

        # Return a JSON response with a success message
        return jsonify({'message': 'All URLs parsed successfully.'})

    except Exception as e:
        traceback.print_exc()  # Add this line to print the exception traceback
        return jsonify({'message': 'Failed to parse URLs.'}), 500


@socketio.on('connect')
def handle_connect():
    print('A user connected')
    # Additional actions when a user connects (e.g., sending initial data to the client)
    emit("YarikTest","Test Hello Yarik")
@socketio.on('my_custom_event')
def handle_custom_event(data):
    # Process the data received from the client
    # Send a response back to the client
    emit('response_event', {'message': 'Data received successfully'})


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
    
