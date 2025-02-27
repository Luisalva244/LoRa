import sqlite3

class Database:

    def initDataBase(self):
        #Use a database outside the directory that has git tracking enabled to avoid conflicts with page.py
        conn = sqlite3.connect('../test.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node INTEGER,
            soilHumidity FLOAT,
            Humidity FLOAT,
            Temperature FLOAT,        
            timestamp TEXT DEFAULT (strftime('%W %Y-%m-%d %H:%M','now','localtime'))     
        )
        ''')
        conn.commit()
        conn.close()

    def writeData(self, data: dict):
        
        conn = sqlite3.connect('../test.db')
        c = conn.cursor()
        c.execute("INSERT INTO data (node, soilHumidity, Humidity, Temperature, timestamp) VALUES (?, ?, ?, ?, datetime('now', 'localtime'))", 
                  (data['node'], data['soilHumidity'], data['Humidity'], data['Temperature']))
        print("[INFO] Guardado en la base de datos:", data)
        conn.commit()
        conn.close()

    def get_all_readings(self):
        conn = sqlite3.connect('/home/luis/Documents/GitHub/test.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, node, soilHumidity, Humidity, Temperature ,timestamp FROM data")
        rows = cursor.fetchall()

        data = []
        for row in rows:
            data.append({
                "id": row[0],
                "node": row[1],
                "soilHumidity": row[2],
                "Humidity": row[3],
                "Temperature": row[4],
                "timestamp": row[5]
            })
        return data
   
if __name__ == "__main__":      
    db = Database()
    db.initDataBase()