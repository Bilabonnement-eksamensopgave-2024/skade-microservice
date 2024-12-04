import sqlite3
import csv

DB_NAME = "damage_reports.db"
TABLE_NAME = "reports"

def create_table():
    with sqlite3.connect(DB_NAME) as conn: 
        cur = conn.cursor() 

        query = f''' 
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        damagereportid INTEGER PRIMARY KEY AUTOINCREMENT,
        carid INTEGER NOT NULL,
        subscriptionid INTEGER NOT NULL,
        reportdate DATE NOT NULL,
        description TEXT NOT NULL, 
        damagetypeid INTEGER NOT NULL
    )'''
    
    cur.execute(query)

def add_csv_file_to_db(filepath):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()

        with open(filepath, 'r', encoding='latin1') as file:
            reader = csv.reader(file)
            headers = next(reader)

            placeholders = ', '.join(['?'] * len(headers))
            query = f"INSERT INTO {TABLE_NAME} ({', '.join(headers)}) VALUES ({placeholders})"
            

            for row in reader:
                cur.execute(query,row)
            
            conn.commit()
            print(f"Data from '{filepath}' has been imported into '{TABLE_NAME}'.")

def get_damage_reports():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM {TABLE_NAME}')

            data = cur.fetchall()

            if data: 
                return [200, [dict(row) for row in data]]
            else:
                return [204, {'message': f'No items in the {TABLE_NAME}'}]
    
    except sqlite3.Error as e:
        return [500, {"error": str(e)}]

def get_damage_reports_by_id(damagereportid : int):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM {TABLE_NAME} WHERE damagereportid = ?', (damagereportid,))
        
            data = cur.fetchone()

            if data is None:
                return [404, {'message': 'Damage report not found'}]
            
            return [200, [dict(data)]]
        
    except sqlite3.Error as e:
        return [500, {"error": str(e)}]

def get_damage_reports_by_carid(carid : int):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM {TABLE_NAME} WHERE carid = ?', (carid,))
        
            data = cur.fetchall()
    
            if not data:
                return [404, {'message': 'Damage report not found'}]
            
            return [200, [dict(row) for row in data]]
        
    except sqlite3.Error as e:
        return [500, {"error": str(e)}]
    
def get_damage_reports_by_subscriptionid(subscriptionid : int):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM {TABLE_NAME} WHERE subscriptionid = ?', (subscriptionid,))
        
            data = cur.fetchall()
    
            if not data:
                return [404, {'message': 'Damage report not found'}]
            
            return [200, [dict(row) for row in data]]
        
    except sqlite3.Error as e:
        return [500, {"error": str(e)}]
    
def get_the_repair_cost_by_subid(subscriptionid: int):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            # Attaches the second database damage_types.db
            cur.execute("ATTACH DATABASE 'damage_type.db' AS damage_type_db;")

            query = f''' 
            SELECT SUM(damage.repair_cost) AS total_amount
            FROM {TABLE_NAME}
            JOIN damage ON {TABLE_NAME}.damagetypeid = damage.id
            WHERE {TABLE_NAME}.subscriptionid = ?'''

            cur.execute(query, (subscriptionid,))
            data = cur.fetchone()

            if data and data[0] is not None: 
                return [200, {"subscriptionid": subscriptionid, "total_amount": data[0]}]
            else:
                return [404, {"message": "No damages found for the given subscription ID"}]
   
    except sqlite3.Error as e:
        return [500, {"error": str(e)}]

#create_table()
#add_csv_file_to_db('damage_reports.csv')