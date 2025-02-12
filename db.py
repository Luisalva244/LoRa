import sqlite3

class Database:

    def initDataBase(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node INTEGER,
            humidity FLOAT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP      
        )
        ''')
        conn.commit()
        conn.close()

    def writeData(self, data: dict):
        
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("INSERT INTO data (node, humidity) VALUES (?, ?)", 
                  (data['node'], data['humidity']))
        print("[INFO] Guardado en la base de datos:", data)
        conn.commit()
        conn.close()