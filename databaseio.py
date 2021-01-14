import sqlite3
import crypto

# Class to handle all sqlite database interaction.
class DatabaseIO():
    def __init__(self):
        self.mycrypto = crypto.Crypto()

    # Function to create the database and to create the tables.

    def create_db(self, database):
        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute(
            """CREATE TABLE entries
                        (name text, username text, 
                        password blob, description text)"""
        )

        c.execute(
            """CREATE TABLE salt
                        (id integer, salt text)"""
        )
        c.execute(
            "INSERT INTO salt VALUES (?,?)",
            (
                0,
                self.mycrypto.generate_salt(),
            ),
        )

        c.execute(
            """CREATE TABLE session
                        (id integer, enc_pass text)"""
        )

        conn.commit()
        conn.close()



    # Function to log into a session.


    def login(self, password, database):
        conn = sqlite3.connect(database)
        c = conn.cursor()

        enc_pass = self.mycrypto.tmp_encrypt(password)

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


    def logout(self, database):
        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute("DELETE FROM session WHERE id=0")

        conn.commit()
        conn.close()


    # Function to read an existing entry.


    def read_entry(self, database, identifier):
        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute("SELECT salt FROM salt WHERE id=0")
        salt = c.fetchone()[0]
        c.execute("SELECT enc_pass FROM session WHERE id=0")
        password = c.fetchone()[0]

        c.execute("SELECT * FROM entries WHERE name=?", (identifier,))
        data = list(c.fetchone())
        data[2] = self.mycrypto.decrypt(data[2], salt, password)

        conn.close()
        return data


    # Function to add a new entry.


    def add_entry(self, database, entry):
        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute("SELECT salt FROM salt WHERE id=0")
        salt = c.fetchone()[0]
        c.execute("SELECT enc_pass FROM session WHERE id=0")
        password = c.fetchone()[0]

        entry["password"] = self.mycrypto.encrypt(entry["password"], salt, password)

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


    def change_or_delete_entry(self, database, identifier, row, change):
        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute("SELECT * FROM salt WHERE id=0")
        salt = c.fetchone()[0]
        c.execute("SELECT enc_pass FROM session WHERE id=0")
        password = c.fetchone()[0]

        if change == None:
            c.execute("DELETE FROM entries WHERE name=?", (identifier,))
            print("Deleted")
        else:
            if row == password:
                change = self.mycrypto.encrypt(change, salt, password)
            c.execute(
                "UPDATE entries SET " + row + "=? WHERE name=?",
                (
                    change,
                    identifier,
                ),
            )
        conn.commit()
        conn.close()