from hashlib import sha512
import mysql.connector
import random
import string

def hash_password(password, salt = "SHAKE"):
    hasher = sha512()
    hasher.update((password + salt).encode())
    return hasher.hexdigest()

def create_session(pk):
    letters = string.ascii_letters + '0123456789'
    session_key = ''.join(random.choice(letters) for i in range(128))
    mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                        host='127.0.0.1', database='diet')
    cursor = mydb.cursor()
    sql = """INSERT INTO sessions (
             pk, session_key
             ) VALUES (%s, %s)"""
    values = (pk, session_key)
    cursor.execute(sql, values)
    mydb.commit()
    return session_key

def lookup_pk_by_session(key):
    mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                        host='127.0.0.1', database='diet')
    cursor = mydb.cursor()
    sql = "SELECT pk FROM sessions WHERE session_key = %s"
    cursor.execute(sql, (key,))
    result = cursor.fetchone()
    if result:
        pk = result[0]
        return pk
    return None