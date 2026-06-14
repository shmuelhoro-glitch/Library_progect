from database.db_connection import db
from logs.logger_app import logger
from fastapi import HTTPException
from database.member_db import MemberDB






class BookDB:
    def __init__(self):
        self.db = db.get_connection

    def create_book_in_db(self,title:str,author:str,genre:str):
        logger.info(f"A request has been sent to add a new book. title:{title} author:{author} genre:{genre.strip()} ")
        with self.db.cursor() as cursor:
            sql_q = "INSERT INTO books (title,author,genre,is_available,borrowed_by_member_id) VALUES (%s,%s,%s,TRUE,NULL);"
            values = (title,author,genre)
            cursor.execute(sql_q,values)
            self.db.commit()
            logger.info(f"The book was added successfully.")
        return True
 
    

        
        

    def get_all_books_in_db(self):
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM books ")
            return cursor.fetchall()


    def get_book_by_id_in_db(self,id:int):
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM books WHERE id = %s ",(id,))
            data = cursor.fetchone()
            return data
            


    def update_book_in_db(self,id:int,update_data):

        keys = [key for key in update_data]
        keys_for_update = ", ".join(f"{key} = %s" for key in keys)
        values = list(update_data.values())
        values.append(id)
        sql_q = "UPDATE books SET " + keys_for_update +" WHERE id = %s"
        print(sql_q,values)

        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute(sql_q,tuple(values))
            self.db.commit()
            return "updated successfully"
        

    def set_available_in_db(self,id:int, val:bool, member_id:int):
        with self.db.cursor() as cursor:
            sql_q = "UPDATE books SET is_available = %s, borrowed_by_member_id = %s WHERE id = %s"
            values = (val,member_id,id)
            cursor.execute(sql_q,values)
            self.db.commit()
            return "updated successfully"
        return False

    def count_total_books_in_db(self):
        with db._connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM books")
            return cursor.fetchone()
            

    def count_available_books_in_db(self):
        with db._connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = True")
            data = cursor.fetchone()
            return data

    def count_borrowed_books_in_db(self):
        with db._connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM books WHERE is_available = False")
            data = cursor.fetchone()
            return data


    def count_by_genre_in_db(self):
        with db._connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT genre as Genre, COUNT(*) AS COUNT FROM books GROUP BY genre")
            return cursor.fetchall()

    def count_active_borrows_by_member_in_db(self,member_id):
        with db._connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) FROM books WHERE borrowed_by_member_id = %s",(member_id,))
            for_return = [num for num in cursor.fetchone().values() if not num is None]
            return int(for_return[0])









