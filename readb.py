from db import Database

db = Database()
db.initDataBase()

# Inserta algo manual


print("Lecturas en BD:")
print(db.get_all_readings())