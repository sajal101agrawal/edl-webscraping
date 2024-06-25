from flask import Flask, request, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

db_ip = "localhost"
db_username = ""
db_pass = ""

client = MongoClient(host=db_ip, username=db_username, password=db_pass)
pfm_db = client.edl_database
collection = pfm_db['edl_collection']

# Load the JSON data once when the server starts
# with open('data.json', 'r') as file:
#     data = json.load(file)

@app.route('/data', methods=['GET'])
def get_data():
    try:
        data = []
        all_data = collection.find({})
        for i in all_data:
            del i['_id']
            data.append(i)
        
        page = int(request.args.get('page', 1))
        per_page = 50
        start = (page - 1) * per_page
        end = start + per_page
        paginated_data = data[start:end]
        
        # Check if there's data for the requested page
        if not paginated_data:
            return jsonify({"error": "Page out of range"}), 404

        response = {
            "page": page,
            "per_page": per_page,
            "total": len(data),
            "total_pages": (len(data) + per_page - 1) // per_page,  # Ceiling division
            "data": paginated_data
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
