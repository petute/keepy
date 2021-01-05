import databaseio, crypto

database = "test.db"
entries = [
    {
        "name": "instagram",
        "username": "tutschi",
        "password": "LetMeIn",
        "description": "bonus info",
    },
    {
        "name": "youtube",
        "username": "tutschi",
        "password": "11supersave11",
        "description": "bonus info",
    },
    {
        "name": "pornhub",
        "username": "tutschi",
        "password": "YouShallPass",
        "description": "bonus info",
    },
    {
        "name": "twitter",
        "username": "tutschi",
        "password": "Passwd",
        "description": "bonus info",
    },
]

# databaseio.createDb(database)
 
databaseio.add_entry(database, entries[0])
# databaseio.add_entry(database, entries[1])
# databasio.add_entry(database, entries[2])
# databaseio.add_entry(database, entries[3])

print(databaseio.read_entry(database, "instagram"))
databaseio.change_or_delete_entry(database, "instagram", "description", "Time consuming nostalgia")
print(databaseio.read_entry(database, "instagram"))
databaseio.change_or_delete_entry(database, "instagram", None, None)
