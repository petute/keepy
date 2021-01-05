import sqlite3
import crypto

# Class to handle all sqlite database interaction.


# Function to create the database and to create the table.


def create_db(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute(
        """CREATE TABLE entries
                    (name text, username text, 
                    password text, description text)"""
    )

    conn.commit()
    conn.close()


# Function to read an existing entry.


def read_entry(database, identifier):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM entries WHERE name=?", (identifier,))
    data = list(c.fetchone())
    data[2] = crypto.decrypt(data[2])

    conn.close()
    return data


# Function to add a new entry.
# TODO: regex


def add_entry(database, entry):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    entry["password"] = crypto.encrypt(entry["password"])

    c.execute(
        "INSERT INTO entries VALUES (?,?,?,?)",
        (
            entry["name"],
            entry["username"],
            entry["password"],
            entry["description"],
        ),
    )

    conn.commit()
    conn.close()


# Function to change or delete an entry (if changes == None).
# TODO: regex


def change_or_delete_entry(database, identifier, row, change):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    if change == None:
        c.execute("DELETE FROM entries WHERE name=?", (identifier,))
        print("Deleted")
    else:
        c.execute(
            "UPDATE entries SET " + row + " = ? WHERE name=?",
            (
                change,
                identifier,
            ),
        )
        print("Updated")

    conn.commit()
    conn.close()