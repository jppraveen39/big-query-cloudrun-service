import logging
import requests
from flask import Flask, request, jsonify
from google.cloud import bigquery
from google.auth import default
import google.auth.transport.requests

app = Flask(__name__)

# Enable detailed error logging
logging.basicConfig(level=logging.DEBUG)

client = bigquery.Client()
PROJECT_ID = "igneous-fold-344311"
DATASET_ID = "test_dataset"
TABLE_ID = "my_table"

# Function to validate the Identity Token
def validate_token(token):
    auth_url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=" + token
    response = requests.get(auth_url)
    return response.status_code == 200

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.before_request
def authenticate_request():
    if "Authorization" not in request.headers:
        return jsonify({"error": "Missing Authorization header"}), 401
    
    token = request.headers["Authorization"].split("Bearer ")[-1]
    if not validate_token(token):
        return jsonify({"error": "Invalid or expired token"}), 403

@app.route("/fetch", methods=["GET"])
def fetch_data():
    try:
        query = f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"
        query_job = client.query(query)
        results = [dict(row) for row in query_job]
        return jsonify(results), 200
    except Exception as e:
        app.logger.error(f"Error in fetch_data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/insert", methods=["POST"])
def insert_data():
    try:
        data = request.json
        if not all(k in data for k in ("name", "age", "email")):
            return jsonify({"error": "Missing required fields"}), 400

        rows_to_insert = [data]
        table_ref = client.dataset(DATASET_ID).table(TABLE_ID)
        errors = client.insert_rows_json(table_ref, rows_to_insert)

        if errors:
            app.logger.error(f"Insert errors: {errors}")
            return jsonify({"error": errors}), 500
        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        app.logger.error(f"Error in insert_data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/delete", methods=["DELETE"])
def delete_data():
    try:
        data = request.json
        if "name" not in data:
            return jsonify({"error": "Missing 'name' field"}), 400

        query = f"DELETE FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` WHERE name = @name"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("name", "STRING", data["name"])]
        )
        query_job = client.query(query, job_config=job_config)
        query_job.result()  # Wait for query to complete

        return jsonify({"message": "Data deleted successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error in delete_data: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

