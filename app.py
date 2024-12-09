#app.py
from flask import Flask, jsonify, request
from damage_type import get_all_damage_types, find_type_by_id, update_type, add_new_types, delete_type_by_id
from dotenv import load_dotenv
from flasgger import swag_from
from swagger.config import init_swagger
import damage_reports
from collections import OrderedDict
import os
import auth

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize Swagger
init_swagger(app)

#---------------------------------------------------------------- 
@app.route('/', methods=['GET'])
def service_info():
    damage_types_service = OrderedDict([
        ("service", "Damage Types Microservice"),
        ("description", "This microservice handles operations related to damage types, such as retrieving, adding, updating, and deleting damage types."),
        ("endpoints", [
            {
                "path": "/damage-types",
                "method": "GET",
                "description": "Retrieve a list of all damage types",
                "role-required": ["admin", "finance", "maintenance"],
                "response": "JSON array of damage type objects"
            },
            {
                "path": "/damage-types/<int:id>",
                "method": "GET",
                "description": "Retrieve a specific damage type by ID",
                "role-required": ["admin", "maintenance"],
                "response": "JSON object of a specific damage type or 404 error"
            },
            {
                "path": "/damage-types",
                "method": "POST",
                "description": "Add a new damage type",
                "role-required": ["admin", "maintenance"],
                "response": "JSON object with success message or error"
            },
            {
                "path": "/damage-types/<int:id>",
                "method": "PATCH",
                "description": "Update an existing damage type by ID",
                "role-required": ["admin", "maintenance"],
                "response": "JSON object with success message or 404 error"
            },
            {
                "path": "/damage-types/<int:id>",
                "method": "DELETE",
                "description": "Delete a damage type by ID",
                "role-required": ["admin", "maintenance"],
                "response": "JSON object with success message or error"
            }
        ])
    ])

    damage_reports_service = OrderedDict([
        ("service", "Damage Report Microservice"),
        ("description", "This microservice handles operations related to damage reports, such as retrieving, adding, updating, and deleting damage reports."),
        ("endpoints", [
            {
                "path": "/damage-reports",
                "method": "GET",
                "description": "Retrieve a list of all damage reports",
                "role-required": ["admin", "maintenance", "finance"],
                "response": "JSON array of damage reports objects"
            },
            {
                "path": "/damage-reports/<int:id>",
                "method": "GET",
                "description": "Retrieve a specific damage report by ID",
                "role-required": ["admin", "maintenance"],
                "response": "JSON object of a specific damage report or error"
            },
            {
                "path": "/damage-reports/cars/<int:id>",
                "method": "GET",
                "description": "Retrieve a specific damage report by Car ID",
                "role-required": ["admin", "maintenance"],
                "response": "JSON object of a specific damage report or error"
            },
            {
                "path": "/damage-reports/subscriptions/<int:id>",
                "method": "GET",
                "description": "Retrieve a specific damage report by Subscription ID",
                "role-required": ["admin", "maintenance"],
                "response": "JSON object of a specific damage report or error"
            },
            {
                "path": "/damage-reports/subscriptions/<int:id>/total-damage",
                "method": "GET",
                "description": "Retrieve the total damage amount for a car by Subscription ID",
                "role-required": ["admin", "finance", "maintenance"],
                "response": "JSON object of the total amount and the subscription ID or 404 error"
            },
            {
                "path": "/damage_reports",
                "method": "POST",
                "description": "Add a new damage report",
                "role-required": ["admin", "maintenance"],
                "response": "JSON object with success message or error"
            },
            {
                "path": "/damage_reports/<int:id>",
                "method": "PATCH",
                "description": "Update an existing damage report by ID",
                "role-required": ["admin", "maintenance"],
                "response": "JSON object with success message or error"
            },
            {
                "path": "/damage_reports/<int:id>",
                "method": "DELETE",
                "description": "Delete a damage report by ID",
                "role-required": ["admin", "maintenance"],
                "response": "JSON object with success message or error"
            }
        ])
    ])

    return jsonify({
        "services": [damage_types_service, damage_reports_service]
    })


# Get all damage types

@app.route('/damage-types', methods=['GET'])
@auth.role_required('admin','finance','maintenance')
@swag_from('swagger/get_damage_types.yaml')
def get_damage_types_route():
    result = get_all_damage_types()
    return jsonify(result[1]), result[0]

#Find type by id
@app.route('/damage-types/<int:id>', methods=['GET'])
@auth.role_required('admin','maintenance')
@swag_from('swagger/get_damage_type_by_id.yaml')
def find_type_by_id_ropute(id):
    result = find_type_by_id(id)

    return jsonify(result[1]), result[0]

#Update damage type
@app.route('/damage-types/<int:id>', methods=['PATCH'])
@auth.role_required('admin','maintenance')
@swag_from('swagger/update_damage_type.yaml')
def update_damage_types(id):
    data = request.json 

    if not data:
        return jsonify({"message": "No data provided"}), 400

    result = update_type(id, data)
    return jsonify(result[1]), result[0]

#Add a damage type
@app.route('/damage-types', methods=['POST'])
@auth.role_required('admin','maintenance')
@swag_from('swagger/add_damage_type.yaml')
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
@app.route('/damage-types/<int:id>', methods=['DELETE'])
@auth.role_required('admin','maintenance')
@swag_from('swagger/delete_damage_type.yaml')
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

#-------------------------------------------------------------Damage Reports routes
# Get all damage reports
@app.route('/damage-reports', methods=['GET'])
@auth.role_required('admin','maintenance','finance')
@swag_from('swagger/get_all_damage_reports.yaml')
def get_all_damage_reports():
    status, data = damage_reports.get_damage_reports()
    return jsonify(data), status

# Get damage report by id 
@app.route('/damage-reports/<int:id>', methods=['GET'])
@auth.role_required('admin','maintenance')
@swag_from('swagger/get_the_selected_damage_report.yaml')
def get_the_selected_damage_report(id):
    status, data = damage_reports.get_damage_reports_by_id(damagereportid=id)
    return jsonify(data), status

# Get damage report by carid
@app.route('/damage-reports/cars/<int:id>', methods=['GET'])
@auth.role_required('admin','maintenance')
@swag_from('swagger/get_the_selected_damage_report_carid.yaml')
def get_the_selected_damage_report_carid(id):
    status, data = damage_reports.get_damage_reports_by_carid(carid=id)
    return jsonify(data), status

# Get damage report by subscriptionsid 
@app.route('/damage-reports/subscriptions/<int:id>', methods=['GET'])
@auth.role_required('admin','maintenance')
@swag_from('swagger/get_the_selected_damage_report_subscriptionid.yaml')
def get_the_selected_damage_report_subscriptionid(id):
    status, data = damage_reports.get_damage_reports_by_subscriptionid(subscriptionid=id)
    return jsonify(data), status

# Total cost for repair by subscription id 
@app.route('/damage-reports/subscriptions/<int:id>/total-cost', methods=['GET'])
@auth.role_required('admin','finance','maintenance')
@swag_from('swagger/get_total_cost_by_subscriptionid.yaml')
def get_total_cost_by_subscriptionid(id):
    status, data = damage_reports.get_the_repair_cost_by_subid(subscriptionid=id)
    return jsonify(data), status

# Total cost for repairs by car id 
@app.route('/cars/<int:id>/total-cost', methods=['GET'])
@auth.role_required('admin','finance','maintenance')
@swag_from('swagger/get_total_cost_by_carid.yaml')
def get_total_cost_by_carid(id):
    status, data = damage_reports.get_the_repair_cost_by_carid(carid=id)
    return jsonify(data), status

# Update damage report 
@app.route('/damage-reports/<int:id>', methods=['PATCH'])
@auth.role_required('admin','maintenance')
@swag_from('swagger/update_damage_report_by_id.yaml')
def update_damage_report_by_id(id):
    update_fields = request.json

    status, data = damage_reports.update_damage_report(damagereportid= id, update_fields= update_fields)

    return jsonify(data), status

# Add new damage report
@app.route('/damage-reports', methods=['POST'])
@auth.role_required('admin','maintenance')
@swag_from('swagger/add_damage_report.yaml')
def add_damage_report():
    data = request.get_json()

    if isinstance(data, dict):
        # Single damage report 
        data = [data]

    if not isinstance(data,list):
        return jsonify({"error": "Invalid input format. Must be a dict or list of dicts."}), 400


    results = []
    for item in data:
        car_id = item.get("carid")
        subscription_id = item.get("subscriptionid")
        report_date = item.get("reportdate")
        description = item.get("description")
        damage_type_id = item.get("damagetypeid")

        if not all ([car_id, subscription_id, report_date, description, damage_type_id]):
            results.append({"status": 400, "response": {"error": "All these fields are required: cardid, subscriptionsid, reportdate, description, damagetypeid"}})
        else:
            status, response_data = damage_reports.add_new_damage_report(
                carid=car_id,
                subscriptionid=subscription_id,
                reportdate=report_date,
                description=description,
                damagetypeid=damage_type_id
            )
            
            results.append({"status": status, "response": response_data})

    return jsonify({"message": "All reports have been processed. Check results to look for failures.", "results": results}), 200

@app.route('/damage-reports/<int:id>', methods=['DELETE'])
@auth.role_required('admin','maintenance')
@swag_from('swagger/delete_damage_report.yaml')
def delete_damage_report (id):
    status, response_data = damage_reports.delete_damage_report(damagereportid=id)
    return jsonify(response_data), status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))