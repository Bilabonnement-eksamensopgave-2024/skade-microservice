from flask import Flask, jsonify, request
from damage_type import get_all_damage_types, find_type_by_id, update_type, add_new_types, delete_type_by_id
import requests

app = Flask(__name__)

# Get all damage types
@app.route('/damage_types', methods=['GET'])
def get_damage_types_route():
    result = get_all_damage_types()
    return jsonify(result[1]), result[0]

#Find type by id
@app.route('/damage_types/<int:id>', methods=['GET'])
def find_type_by_id_ropute(id):
    result = find_type_by_id(id)

    return jsonify(result[1]), result[0]

#Update damage type
@app.route('/damage_types/<int:id>', methods=['PATCH'])
def update_damage_types(id):
    data = request.json 

    if not data:
        return jsonify({"message": "No data provided"}), 400

    result = update_type(id, data)
    return jsonify(result[1]), result[0]

#Add a damage type
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



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)