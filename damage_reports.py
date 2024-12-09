#damage_reports.py
import sqlite3
import csv
from datetime import date
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
DB_PATH = os.getenv('DB_PATH', "damage.db")
TABLE_NAME = "damage_reports"

def create_table():
    with sqlite3.connect(DB_PATH) as conn: 
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
    with sqlite3.connect(DB_PATH) as conn:
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
        with sqlite3.connect(DB_PATH) as conn:
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
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM {TABLE_NAME} WHERE damagereportid = ?', (damagereportid,))
        
            data = cur.fetchone()

            if data is None:
                return [404, {'message': 'Damage report not found'}]
            
            return [200, dict(data)]
        
    except sqlite3.Error as e:
        return [500, {"error": str(e)}]

def get_damage_reports_by_carid(carid : int):
    try:
        with sqlite3.connect(DB_PATH) as conn:
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
        with sqlite3.connect(DB_PATH) as conn:
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
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

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
    
def update_damage_report(damagereportid: int, update_fields: dict): 
    try: 
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            set_clause = ", ".join(f'{key} = ?' for key in update_fields.keys())
            values = list(update_fields.values()) + [damagereportid]
            
            query = f'''
            UPDATE {TABLE_NAME}
            SET {set_clause}
            WHERE damagereportid = ? '''

            cur.execute(query, values)

            if cur.rowcount > 0: 
                conn.commit()
                return [200, {"message": "Damage report updated successfully", "damage_report_id": damagereportid}]
            else: 
                return [404, {"message": "Damage report not found"}]
    
    except sqlite3.Error as e:
        return [500, {"error": str(e)}]
    

def add_new_damage_report(
        carid: int, subscriptionid: int, reportdate: date, 
        description: str, damagetypeid: int ):
    try:
        with sqlite3.connect(DB_PATH) as conn: 
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            query = f'''
            INSERT INTO {TABLE_NAME} ( carid, subscriptionid, reportdate,
            description, damagetypeid) 
            VALUES (?,?,?,?,?)
            '''

            cur.execute(query, (carid,subscriptionid,reportdate,description,damagetypeid))
            conn.commit()

            return [200, {'message': 'New damage report added succesfully'}]
    
    except sqlite3.IntegrityError:
        return [409, {"error": "Damage report already exists with these details."}]
    except sqlite3.Error as e:
        return [500, {"error": str(e)}]    
  
def delete_damage_report(damagereportid):
    try:
        with sqlite3.connect(DB_PATH) as conn: 
            cur = conn.cursor()

            delete_query = f'DELETE FROM {TABLE_NAME} WHERE damagereportid = ?'
            cur.execute(delete_query, (damagereportid,))
            
            if cur.rowcount == 0: 
                return [404, {"message": "Damage report not found"}]
            
            cur.execute(f"UPDATE sqlite_sequence SET seq = (SELECT MAX(damagereportid) FROM {TABLE_NAME} WHERE name = '{TABLE_NAME}')")
            conn.commit()


            return [200, {"message": "Damage report deleted successfully and ID sequence reset"}]
    
    except sqlite3.Error as e:
        return [500, {"error": str(e)}]



create_table()
#add_csv_file_to_db('damage_reports.csv')