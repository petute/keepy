from os import path, remove
import databaseio

mydb = databaseio.DatabaseIO()
__database_name = ""

# Function to display some help text
def help():
    print("If you are new you have to setup a new database!\n" +
    "You can login to one database with many passwords but you have to remember" + 
    " which entry works with what password (to maybe be changed)\n" +
    "Here is a list of available commands:\n" +
    "  create_db <name>                               Creates new Database.\n" +
    "  delete_db <name>                               Deletes Database.\n" +
    "  login <database_name> <password>               Logs you into existing Database.\n" +
    "  logout                                         Logs you out of current Database.\n" +
    "  add <name> <username> <password> <description> Add a new entry.\n" +
    "  change <entry_name> <field_to_change> <change> Change a field of an entry." + 
    "Field to change is password, name etc.\n" +
    "  delete <name>                                  Delete entry.\n" +
    "  read <name>                                    Read an entry.")

# Function that calls the function that creates a database :)
def create_db(database):
    if path.exists(database):
        print("Database already exists!")
    else:
        if(database.split(".")[-1] != "sqlite"):
            mydb.create_db(database + ".sqlite")
        else:
            mydb.create_db(database)
        print("Database " + database + " created!")

# Interface function to delete a database
def delete_db(database):
    if(database.split(".")[-1] != "sqlite"):
        remove(database + ".sqlite")
    else:
        remove(database)
    print("Database " + database + " removed!")

# Interface function to log into a database
def login(password, database):
    if (path.exists(database + ".sqlite") and database.split(".")[-1] != "sqlite" 
        or path.exists(databae) and databse.split(".")[-1] == "sqlite"):
        global database_name
        database_name = database
        mydb.login(password, database + ".sqlite")
        print("Logged in")
    else:
        print("Database does not exist.")

# Interface function to logout
def logout():
    if database_name != "":
        mydb.logout()
        print("Logged out")
    else:
        print("Could not logout!")

# Interface function to add an new entry
def add(name, username, password, description):
    if database_name == "":
        print("Please log into a database first.")
    else:
        mydb.add_entry(name, username, password, description)
        print("Added Entry")

# Interface function to change a field of an entry
def change(name, row, change):
    if database_name == "":
        print("Please log into a database first.")
    else:
        mydb.change_or_delete_entry(name, row, change)

# Interface function to delete an entry
def delete(name):
    if database_name == "":
        print("Please log into a database first.")
    else:
        mydb.change_or_delete_entry(name, None, None)

# Interdace function to read entry
def read(name):
    if database_name == "":
        print("Please log into a database first.")
    else:
        print(mydb.read_entry(name))



# Welcome message
print("Welcome to keepy. Your shitty python keymanager!")
print("To get an overview of the available commands type help, to quit type quit or q\n")

# Loop to get input
while True:
    user_input = input()
    user_input = user_input.split(" ")
    if user_input[0] == "help":
        help()
    elif user_input[0] == "quit" or user_input[0] == "q":
        break
    elif user_input[0] == "create_db" and len(user_input) == 2:
        create_db(user_input[1])
    elif user_input[0] == "delete_db" and len(user_input) == 2:
        delete_db(user_input[1])
    elif user_input[0] == "login" and len(user_input) == 3:
        login(user_input[2], user_input[1])
    elif user_input[0] == "logout" and len(user_input) == 1:
        logout()
    elif user_input[0] == "add" and len(user_input) == 5:
        add(user_input[1], user_input[2], user_input[3], user_input[4])
    elif user_input[0] == "change" and len(user_input) == 4:
        change(user_input[1], user_input[2], user_input[3])
    elif user_input[0] == "delete" and len(user_input) == 2:
        delete(user_input[1])
    elif user_input[0] == "read" and len(user_input) == 2:
        read(user_input[1])
    else:
        print("Command not available or wrong use. For list of commands type 'help'")

logout()