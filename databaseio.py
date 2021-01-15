import sqlite3
import crypto

# Class to handle all sqlite database interaction.
class DatabaseIO():
    def __init__(self):
        self.mycrypto = crypto.Crypto()
        self.database = ""

    # Function to create the database and to create the tables.
    def create_db(self, database):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        cursor.execute(
            """CREATE TABLE entries
                        (name text, username text, 
                        password blob, description text)"""
        )

        cursor.execute(
            """CREATE TABLE salt
                        (id integer, salt blob)"""
        )
        cursor.execute(
            "INSERT INTO salt VALUES (?,?)",
            (
                0,
                self.mycrypto.generate_salt(),
            ),
        )

        cursor.execute(
            """CREATE TABLE session
                        (id integer, enc_pass text)"""
        )

        conn.commit()
        conn.close()

    # Function to log into a session.
    def login(self, password, database):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        self.database = database
        enc_pass = self.mycrypto.tmp_encrypt(password)

        # In case the program wasn't closed properly
        cursor.execute("DELETE FROM session WHERE id=0")

        cursor.execute(
            "INSERT INTO session VALUES (?,?)",
            (
                0,
                enc_pass,
            ),
        )

        conn.commit()
        conn.close()

    # Function to logout of a session.
    def logout(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        self.database = ""
        cursor.execute("DELETE FROM session WHERE id=0")

        conn.commit()
        conn.close()

    # Function to read an existing entry.
    def read_entry(self, identifier):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        cursor.execute("SELECT salt FROM salt WHERE id=0")
        salt = cursor.fetchone()[0]
        cursor.execute("SELECT enc_pass FROM session WHERE id=0")
        password = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM entries WHERE name=?", (identifier,))
        data = cursor.fetchall()
        if data != []:
            data = list(data[0])
            data[2] = self.mycrypto.decrypt(data[2], salt, password)
            data[2] = data[2].decode('UTF-8')
        else:
            data = "Can not read an nonexistant entry"
        conn.close()
        return data

    # Function to add a new entry.
    def add_entry(self, name, username, password, description):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        cursor.execute("SELECT salt FROM salt WHERE id=0")
        salt = cursor.fetchone()[0]
        cursor.execute("SELECT enc_pass FROM session WHERE id=0")
        enc_password = cursor.fetchone()[0]

        password = self.mycrypto.encrypt(password, salt, enc_password)

        cursor.execute(
            "INSERT INTO entries VALUES (?,?,?,?)",
            (
                name,
                username,
                password,
                description,
            ),
        )
        conn.commit()
        conn.close()

    # Function to change or delete an entry (if changes == None).
    def change_or_delete_entry(self, identifier, row, change):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        cursor.execute("SELECT salt FROM salt WHERE id=0")
        salt = cursor.fetchone()[0]
        cursor.execute("SELECT enc_pass FROM session WHERE id=0")
        enc_password = cursor.fetchone()[0]

        if change == None:
            cursor.execute("DELETE FROM entries WHERE name=?", (identifier,))
        else:
            if row == "password":
                change = self.mycrypto.encrypt(change, salt, enc_password)
            cursor.execute(
                "UPDATE entries SET " + row + "=? WHERE name=?",
                (
                    change,
                    identifier,
                ),
            )
        conn.commit()
        conn.close()
