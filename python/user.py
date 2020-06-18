import mysql.connector
from .util import hash_password
from .plan import Plan

class User:

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.email = kwargs.get("email")
        self.password_hash = kwargs.get("password_hash")

    def save(self):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = """INSERT INTO users (
                 email, password_hash
                 ) VALUES (%s, %s)"""
        self.password_hash = hash_password(self.password_hash)
        values = (self.email, self.password_hash)
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
    def login(cls, email, password):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = "SELECT * FROM users WHERE email = %s AND password_hash = %s"
        values = (email, hash_password(password))
        cursor.execute(sql, values)
        result = cursor.fetchone()
        if result:
            return cls(pk=result[0], email=result[1], password_hash=result[2])
        return None

    def get_plan(self):
        plan = Plan.plan_for_user(self.pk)
        return plan
    