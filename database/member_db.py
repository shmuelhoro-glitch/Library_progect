from database.db_connection import db





class MemberDB():
    def __init__(self):
        self.db = db.get_connection

    
    def create_member_in_db(self,name:str,email:str):
        with self.db.cursor() as cursor:
            sql_q = "INSERT INTO members (name, email) VALUES (%s, %s);"
            values = (name,email)
            cursor.execute(sql_q,values)
            self.db.commit()
            return "created successfully "

    def get_all_members_in_db(self):
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM members ")
            return cursor.fetchall()



    def get_member_by_id_in_db(self,id):
         with self.db.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM members WHERE id = %s",(id,))
            return cursor.fetchone()



    def update_member_in_db(self,id,data):
        keys = ", ".join(f"{key} = %s" for key in data.keys())
        values = list(data.values())
        values.append(id)
        sql_q = "UPDATE members SET " + keys + " WHERE id = %s"
        with self.db.cursor() as cursor:
            cursor.execute(sql_q,tuple(values))
            self.db.commit()
        return "updated successfully"




    def deactivate_member_in_db(self,id):
        with self.db.cursor() as cursor:
            cursor.execute("UPDATE members SET is_active = False WHERE id = %s",(id,))
            self.db.commit()
            return "success"




    def activate_member_in_db(self,id):
        with self.db.cursor() as cursor:
            cursor.execute("UPDATE members SET is_active = True WHERE id = %s",(id,))
            self.db.commit()
            return "success"




    def increment_borrows_in_db(self,id:int):
        with self.db.cursor() as cursor:
            cursor.execute("UPDATE members SET total_borrows = total_borrows +1 WHERE id = %s",(id,))
            self.db.commit()
            return


    def count_active_members_in_db(self):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM members WHERE is_active = True")
            return cursor.fetchone()

    def get_top_member_in_db(self):
         with self.db.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM members ORDER BY total_borrows DESC LIMIT 1")
            return cursor.fetchone()

































