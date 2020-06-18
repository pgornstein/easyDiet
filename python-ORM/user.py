import mysql.connector
from util import hash_password
from plan import Plan

class User:

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")
        self.password_hash = kwargs.get("password")

    def save(self):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = """INSERT INTO users (
                 name, email, password_hash
                 ) VALUES (%s, %s, %s)"""
        self.password_hash = hash_password(self.password_hash)
        values = (self.name, self.email, self.password_hash)
        cursor.execute(sql, values)
        mydb.commit()

    def delete(self):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = "DELETE FROM users WHERE pk = %s"
        cursor.execute(sql, (self.pk,))
        mydb.commit()

    @classmethod
    def exists_user_with_email(cls, email):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = "SELECT * FROM users WHERE email = %s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        if result:
            return True
        return False

    @classmethod
    def login(cls, email, password):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = "SELECT * FROM users WHERE email = %s AND password_hash = %s"
        values = (email, hash_password(password))
        cursor.execute(sql, values)
        result = cursor.fetchone()
        if result:
            return cls(pk=result[0], name=result[1], email=result[2], 
                       password_hash=result[3])
        return None

    @classmethod
    def user_for_pk(cls, pk):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = "SELECT * FROM users WHERE pk = %s"
        cursor.execute(sql, (pk,))
        result = cursor.fetchone()
        if result:
            return cls(pk=result[0], name=result[1], email=result[2], 
                       password_hash=result[3])
        return None

    def get_plan(self):
        plan = Plan.plan_for_user(self.pk)
        return plan
    