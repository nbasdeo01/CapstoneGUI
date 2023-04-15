import sqlite3
from sqlite3 import Error

# users
def add_new_user(cur, id, password, is_admin):
    cur.execute(f"""
            INSERT INTO
                USERS
            VALUES 
                (?,?,?,?)
            ;""", (None, id, password, is_admin))
    return

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = "pythonsqlite.db"

    sql_create_USERS_table = """ CREATE TABLE IF NOT EXISTS USERS (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    user_id string NOT NULL,
                                    passcode string NOT NULL,
                                    is_admin integer NOT NULL
                                    ); """

    sql_create_ITEMS_table = """CREATE TABLE IF NOT EXISTS ITEMS (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    name text NOT NULL,
                                    price REAL NOT NULL,
                                    quantity integer NOT NULL
                                );"""

    sql_create_TRANSACTIONS_table = """CREATE TABLE IF NOT EXISTS TRANSACTIONS (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    items text NOT NULL,
                                    sub_total REAL NOT NULL,
                                    time text NOT NULL,
                                    user_id string NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES USERS (id)
                                );"""
    
    sql_create_EMPLOYEE_TIME_table = """CREATE TABLE IF NOT EXISTS EMPLOYEE_TIME (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        employee_id INTEGER NOT NULL,
                                        timestamp TEXT NOT NULL,
                                        FOREIGN KEY (employee_id) REFERENCES employees (id)
                                        );"""

    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create users, tasks, and transactions tables
        create_table(conn, sql_create_USERS_table)
        create_table(conn, sql_create_ITEMS_table)
        create_table(conn, sql_create_TRANSACTIONS_table)
        create_table(conn, sql_create_EMPLOYEE_TIME_table)
        cur = conn.cursor()

        add_new_user(cur, "1111", "2222", 1)
        add_new_user(cur, "3333", "4444", 1)
        add_new_user(cur, "5555", "6666", 0)
        add_new_user(cur, "7777", "8888", 0)
        conn.commit()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()