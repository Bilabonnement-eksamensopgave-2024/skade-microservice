import sqlite3
import csv

DB_NAME = 'damage_type.db'
TABLE_NAME = 'damage'

def create_table():
    with sqlite3.connect(DB_NAME) as conn:
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
    with sqlite3.connect(DB_NAME) as conn:
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
        with sqlite3.connect(DB_NAME) as conn:
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
        with sqlite3.connect(DB_NAME) as conn:
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







#create_table()
#add_csv_to_db('damage_types.csv')
