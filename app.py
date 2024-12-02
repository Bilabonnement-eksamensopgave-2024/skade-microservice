from flask import Flask, jsonify, request
from damage_type import get_all_damage_types, find_type_by_id
import requests

app = Flask(__name__)

# Get all damage types
@app.route('/get_damage_types', methods=['GET'])
def get_damage_types_route():
    result = get_all_damage_types()
    return jsonify(result[1]), result[0]

#Find type by id
@app.route('/get_damage_type_by_id/<int:id>', methods=['GET'])
def find_type_by_id_ropute(id):
    result = find_type_by_id(id)

    return jsonify(result[1]), result[0]



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)