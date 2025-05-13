import sqlite3  
  
def get_db_connection():  
    conn = sqlite3.connect(':memory:')  
    cursor = conn.cursor()  
    cursor.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")  
    cursor.execute("INSERT INTO items (name) VALUES ('item1'), ('item2'), ('item3')")  
    conn.commit()  
    return conn  