import sqlite3

def read_data():
    """
    Lee todos los registros de la tabla 'data' en test.db 
    y retorna una lista de tuplas (id, node, humidity, timestamp).
    """
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT id, node, humidity, timestamp FROM data")
    rows = c.fetchall()  # Obtiene todos los resultados
    conn.close()
    return rows

def main():
    registros = read_data()
    if not registros:
        print("No hay datos en la tabla 'data'.")
        return
    
    print("Registros en la tabla 'data':")
    for row in registros:
        # row es una tupla (id, node, humidity, timestamp)
        print(f"ID: {row[0]}, Node: {row[1]}, Humedad: {row[2]}, Timestamp: {row[3]}")

if __name__ == "__main__":
    main()