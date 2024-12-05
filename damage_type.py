import sqlite3
import csv
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
DB_PATH = os.getenv('DB_PATH', "damage.db")
TABLE_NAME = 'damage_type'

def create_table():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        damage_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        repair_cost INTEGER NOT NULL
    )
    '''
        
    cur.execute(create_table_query)



def add_csv_to_db(filepath):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        
        with open(filepath, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header
            
            for line in csv_reader:
                cur.execute(f"""
                INSERT INTO {TABLE_NAME} (id, damage_type, severity, repair_cost)
                VALUES (?, ?, ?, ?)
                """, (int(line[0]), line[1], line[2], int(line[3])))

def get_all_damage_types():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM {TABLE_NAME}')

            data = cur.fetchall()
        
            if data:
                return [200, [dict(row) for row in data]]
            else:
                return [204, {"message": f"No types in {TABLE_NAME}"}]
    
    except sqlite3.Error as e:
        return [500, {"error": str(e)}]

def find_type_by_id(id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            cur.execute(f'SELECT * FROM {TABLE_NAME} WHERE id = ?', (id,))
            data = cur.fetchone()  
            
            if data:
                return [200, dict(data)]  
            else:
                return [404, {"message": "type not found"}]
    
    except sqlite3.Error as e:
        return [500, {"error": str(e)}]

def update_type(id, data):
    try:
        if not data:
            return [400, {"message": "No data provided for update."}]

        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()

            
            query = f"UPDATE {TABLE_NAME} SET "
            updates = []
            values = []

            for key, value in data.items():
                if key != "id":  
                    updates.append(f"{key} = ?")
                    values.append(value)

            query += ", ".join(updates)
            query += " WHERE id = ?"
            values.append(id) 

            cur.execute(query, values)

            if cur.rowcount == 0:
                return [404, {"message": "Damage type not found."}]

            return [200, {"message": "Damage type updated successfully."}]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]

def add_new_types(data):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()

            # Check if ID is provided in the data
            if "id" in data and data["id"] is not None:
                cur.execute(
                    f'''
                    INSERT OR IGNORE INTO {TABLE_NAME}
                    (id, damage_type, severity, repair_cost)
                    VALUES (?, ?, ?, ?)
                    ''',
                    (
                        data["id"],
                        data["damage_type"],
                        data["severity"],
                        data["repair_cost"]
                    )
                )
            else:
                # Insert without ID, letting the database auto-assign it
                cur.execute(
                    f'''
                    INSERT INTO {TABLE_NAME}
                    (damage_type, severity, repair_cost)
                    VALUES (?, ?, ?)
                    ''',
                    (
                        data["damage_type"],
                        data["severity"],
                        data["repair_cost"]
                    )
                )

            if cur.rowcount == 0:
                return [409, {"message": "Type already exists in the database."}]
            
            return [201, {"message": "New type added to database successfully."}]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]

def delete_type_by_id(id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()

            # Delete the row with the specified id
            cur.execute(f'DELETE FROM {TABLE_NAME} WHERE id = ?', (id,))
            
            if cur.rowcount == 0:
                return [404, {"message": "Type not found."}]
            
            return [204, {"message": f"Type deleted from {TABLE_NAME} successfully."}]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]


create_table()
#add_csv_to_db('damage_types.csv')
