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


#create_table()
#add_csv_to_db('damage_types.csv')
