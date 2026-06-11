import mysql.connector
from logs.logger_app import logger


class Connection_db:
    def __init__(self):
        self.conn = self.connection()

    def connection(self):
        self.conn =  mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "root",
                database = "library_db"
            )
    def get_connection(self):
        if self.conn.is_connected:
            return self.conn
        else:
            self.conn = self.connection()
            return self.conn


    def create_tables(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS books (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(50) NOT NULL, author VARCHAR(50) NOT NULL, genre ENUM( 'Fiction', 'Non-Fiction', 'Science', 'History', 'Other' ) NOT NULL , is_available BOOLEAN DEFAULT TRUE NOT NULL, borrowed_by_member_id INT DEFAULT NULL)")
        self.conn.commit()
        if self.cursor.rowcount > 0:
            logger.warning("The books table has just been created.")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS members (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50) NOT NULL, email VARCHAR(50) UNIQUE NOT NULL, is_active BOOLEAN DEFAULT TRUE NOT NULL, total_borrows INT NOT NULL)")
        self.conn.commit()
        if self.cursor.rowcount > 0:
            logger.warning("The members table has just been created.")
        return

