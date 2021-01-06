import sqlite3
from crypto import Crypto as crypto

# Class to handle all sqlite database interaction.


# Function to create the database and to create the tables.


def create_db(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute(
        """CREATE TABLE entries
                    (name text, username text, 
                    password text, description text)"""
    )

    c.execute(
        """CREATE TABLE salt
                    (id integer, salt text)"""
    )
    c.execute(
        "INSERT INTO salt VALUES (?,?)",
        (
            0,
            crypto.setup(),
        ),
    )

    c.execute(
        """CREATE TABLE session
                    (id integer, enc_pass text)"""
    )

    conn.commit()
    conn.close()


# Function to log into a session.


def login(password, database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    enc_pass = crypto.tmp_encrypt(password)

    # In case the program wasn't closed properly
    c.execute("DELETE FROM session WHERE id=0")

    c.execute(
        "INSERT INTO session VALUES (?,?)",
        (
            0,
            enc_pass,
        ),
    )

    conn.commit()
    conn.close()


# Function to logout of a session.


def logout(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("DELETE FROM session WHERE id=0")

    print("Logged out")
    conn.commit()
    conn.close()


# Function to read an existing entry.


def read_entry(database, identifier):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM salt WHERE id=0")
    salt = list(c.fetchone())

    c.execute("SELECT * FROM entries WHERE name=?", (identifier,))
    data = list(c.fetchone())
    data[2] = crypto.decrypt(data[2], salt[1])

    conn.close()
    return data


# Function to add a new entry.


def add_entry(database, entry):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM salt WHERE id=0")
    salt = list(c.fetchone())

    entry["password"] = crypto.encrypt(entry["password"], salt[1])

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

# TODO encrypt if password


def change_or_delete_entry(database, identifier, row, change):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM salt WHERE id=0")
    salt = list(c.fetchone())

    if change == None:
        c.execute("DELETE FROM entries WHERE name=?", (identifier,))
        print("Deleted")
    else:
        c.execute(
            "UPDATE entries SET " + row + "=? WHERE name=?",
            (
                change,
                identifier,
            ),
        )
        print("Updated")

    conn.commit()
    conn.close()