from flask import Flask, jsonify, request
from damage_type import get_all_damage_types, find_type_by_id, update_type, add_new_types, delete_type_by_id
import requests
import sqlite3
import bcrypt
import os
import jwt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
from flasgger import swag_from
import datetime
from swagger.config import init_swagger
import damage_reports
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize Swagger
init_swagger(app)

#---------------------------------------------------------------- 
@app.route('/', methods=['GET'])
def service_info():
    return jsonify({
        "service": "Damage Types Microservice",
        "description": "This microservice handles operations related to damage types, such as retrieving, adding, updating, and deleting damage types.",
        "endpoints": [
            {
                "path": "/damage_types",
                "method": "GET",
                "description": "Retrieve a list of all damage types",
                "response": "JSON array of damage type objects"
            },
            {
                "path": "/damage_types/<int:id>",
                "method": "GET",
                "description": "Retrieve a specific damage type by ID",
                "response": "JSON object of a specific damage type or 404 error"
            },
            {
                "path": "/damage_types",
                "method": "POST",
                "description": "Add a new damage type",
                "response": "JSON object with success message or error"
            },
            {
                "path": "/damage_types/<int:id>",
                "method": "PATCH",
                "description": "Update an existing damage type by ID",
                "response": "JSON object with success message or 404 error"
            },
            {
                "path": "/damage_types/<int:id>",
                "method": "DELETE",
                "description": "Delete a damage type by ID",
                "response": "JSON object with success message or 404 error"
            }
        ]
    })

# Get all damage types
#@role_required('user') # TODO UPDATE LATER
@app.route('/damage_types', methods=['GET'])
def get_damage_types_route():
    result = get_all_damage_types()
    return jsonify(result[1]), result[0]

#Find type by id
#@role_required('user') # TODO UPDATE LATER
@app.route('/damage_types/<int:id>', methods=['GET'])
def find_type_by_id_ropute(id):
    result = find_type_by_id(id)

    return jsonify(result[1]), result[0]

#Update damage type
#@role_required('user') # TODO UPDATE LATER
@app.route('/damage_types/<int:id>', methods=['PATCH'])
def update_damage_types(id):
    data = request.json 

    if not data:
        return jsonify({"message": "No data provided"}), 400

    result = update_type(id, data)
    return jsonify(result[1]), result[0]

#Add a damage type
#@role_required('user') # TODO UPDATE LATER
@app.route('/damage_types', methods=['POST'])
def add_to_types():
    data = request.json

    if not data:
        return jsonify({"message": "No data provided"}), 400

    try:
        damage_type_item = _data_to_damage_type_dict(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    result = add_new_types(damage_type_item)
    return jsonify(result[1]), result[0]

# Delete type form table
#@role_required('user') # TODO UPDATE LATER
@app.route('/damage_types/<int:id>', methods=['DELETE'])
def delete_type_from_damage_type(id):

    result = delete_type_by_id(id)
    return jsonify(result[1]), result[0]



def _data_to_damage_type_dict(data):
    if not all(key in data for key in ["damage_type", "severity", "repair_cost"]):
        raise ValueError("Missing required fields in data.")
    
    return {
        "id": int(data["id"]) if "id" in data and data["id"] else None,
        "damage_type": data["damage_type"],
        "severity": data["severity"],
        "repair_cost": int(data["repair_cost"]) if data["repair_cost"] else None,
    }

#-------------------------------------------------------------Damage Reports
# Get all damage reports
@app.route('/damage-reports', methods=['GET'])
def get_all_damage_reports():
    status, data = damage_reports.get_damage_reports()
    return jsonify(data), status

# Get damage report by id 
@app.route('/damage-reports/<int:id>', methods=['GET'])
def get_the_selected_damage_report(id):
    status, data = damage_reports.get_damage_reports_by_id(damagereportid=id)
    return jsonify(data), status

# Get damage report by carid
@app.route('/damage-reports/cars/<int:id>', methods=['GET'])
def get_the_selected_damage_report_carid(id):
    status, data = damage_reports.get_damage_reports_by_carid(carid=id)
    return jsonify(data), status

# Get damage report by subscriptionsid 
@app.route('/damage-reports/subscriptions/<int:id>', methods=['GET'])
def get_the_selected_damage_report_subscriptionid(id):
    status, data = damage_reports.get_damage_reports_by_subscriptionid(subscriptionid=id)
    return jsonify(data), status

# Total amount for repair cost by subscription id 
@app.route('/damage-reports/subscriptions/<int:id>/total-damage', methods=['GET'])
def get_total_cost_by_subscriptionid(id):
    status, data = damage_reports.get_the_repair_cost_by_subid(subscriptionid=id)
    return jsonify(data), status


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)