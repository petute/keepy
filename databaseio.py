import sqlite3
import crypto

# Class to handle all sqlite database interaction.


# Function to create database and to create the table.


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


# Function to read existing entry.


def read_entry(database, identifier):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM entries WHERE name=?", (identifier,))
    data = list(c.fetchone())
    data[2] = crypto.decrypt(data[2])
    return data

    conn.close()


