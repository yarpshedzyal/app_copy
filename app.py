from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient, UpdateOne
from bson.objectid import ObjectId
from flask import jsonify
from libs.parser_1.other_module import parser_solo
import os
# import pymongo
# import libraryparse

app = Flask(__name__)

client = MongoClient('mongodb+srv://user_yarpshe:Q1w2e3r4_0@cluster0.aktya2j.mongodb.net/')
db = client['test_1506']
collection = db['test']

@app.route('/')
def index():
    urls = collection.find({}, {"_id": 1, "SKU": 1, "Link": 1, "Price": 1, "Stock": 1})
    return render_template('index.html', urls=urls)

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
    # Get all the URLs from MongoDB
    urls = collection.find()

    # Iterate over each URL and perform parsing using Selenium
    for url in urls:
        url_id = str(url['_id'])
        link = url['Link']

        # Perform parsing using the parser_solo function
        parsed_data = parser_solo(link)

        # Update the document in MongoDB with the parsed data
        collection.update_one(
            {'_id': ObjectId(url_id)},
            {'$set': {'Price': parsed_data[0], 'Stock': parsed_data[1]}}
        )

    # Return a JSON response with a success message
    return jsonify({'message': 'All URLs parsed successfully.'})




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))