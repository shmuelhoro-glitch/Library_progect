import mysql.connector
from logs.logger_app import logger



class DB:
    def __init__(self):
        self._connection = None
        self.connect()
        self.init_db()
        self.init_tables()
    


    def connect(self):
        self._connection =  mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "root",
                database = "library_db"
            )
        

    def init_db(self):
        cursor = self._connection.cursor()
        cursor.execute("""CREATE DATABASE IF NOT EXISTS library_db""")
        cursor.execute("USE library_db")
        cursor.close()

    
    def init_tables(self):
        cursor = self._connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS books (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(50) NOT NULL, author VARCHAR(50) NOT NULL, genre ENUM( 'Fiction', 'Non-Fiction', 'Science', 'History', 'Other' ) NOT NULL , is_available BOOLEAN DEFAULT TRUE NOT NULL, borrowed_by_member_id INT DEFAULT NULL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS members (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50) NOT NULL, email VARCHAR(50) UNIQUE NOT NULL, is_active BOOLEAN DEFAULT TRUE NOT NULL, total_borrows INT NOT NULL DEFAULT 0 )")
        cursor.close()

    @property
    def get_connection(self):
        if not self._connection.is_connected():
            self.connect()
        return self._connection
    

try:
    db = DB()
except Exception as e:
    print(e)
    raise 


