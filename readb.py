from db import Database

db = Database()
db.initDataBase()

# Inserta algo manual
db.writeData({
    "node": 99,
    "humidity": 44.4
})

print("Lecturas en BD:")
print(db.get_all_readings())