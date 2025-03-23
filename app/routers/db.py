import sqlite3

class Database:

    def initDataBase(self):
        #Use a database outside the directory that has git tracking enabled to avoid conflicts with page.py
        conn = sqlite3.connect('/home/luis/Documents/GitHub/test.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS data(
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
        
        conn = sqlite3.connect('/home/luis/Documents/GitHub/test.db')
        c = conn.cursor()
        c.execute("INSERT INTO data (node, soilHumidity, Humidity, Temperature, timestamp) VALUES (?, ?, ?, ?, strftime('%W %Y-%m-%d %H:%M','now','localtime'))", 
                  (data['node'], data['soilHumidity'], data['Humidity'], data['Temperature']))
        print("[INFO] Guardado en la base de datos:", data)
        conn.commit()
        conn.close()

    def get_all_readings(self):
        conn = sqlite3.connect('/home/luis/Documents/GitHub/test.db')
        cursor = conn.cursor()
        cursor.execute("SELECT node, soilHumidity, Humidity, Temperature ,timestamp FROM data")
        rows = cursor.fetchall()

        data = []
        for row in rows:
            data.append({
                "node": row[0],
                "soilHumidity": row[1],
                "Humidity": row[2],
                "Temperature": row[3],
                "timestamp": row[4]
            })
        return data
   
if __name__ == "__main__":      
    db = Database()
    db.initDataBase()