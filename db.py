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

    def get_all_readings(self):
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, node, humidity, timestamp FROM data")
        rows = cursor.fetchall()
        conn.close()

        data = []
        for row in rows:
            data.append({
                "id": row[0],
                "node": row[1],
                "humidity": row[2],
                "timestamp": row[3]
            })
        return data
   