import mysql.connector

def schema():
    mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                        host='127.0.0.1', database='diet')
    cursor = mydb.cursor()
    # Create the users table
    sql = """CREATE TABLE IF NOT EXISTS users (
             pk INT AUTO_INCREMENT PRIMARY KEY,
             email VARCHAR(50) NOT NULL,
             password_hash VARCHAR(128) NOT NULL 
             );"""
    cursor.execute(sql)

    # Create the plans table
    sql = """CREATE TABLE IF NOT EXISTS plans (
             pk INT AUTO_INCREMENT PRIMARY KEY,
             user_pk INT,
             continuous BOOL NOT NULL,
             start_date DATE NOT NULL,
             end_date DATE,
             type VARCHAR(50) NOT NULL,
             breakfast_time TIME NOT NULL,
             lunchtime TIME NOT NULL,
             dinnertime TIME NOT NULL,
             calorie_limit INT NOT NULL,
             FOREIGN KEY (user_pk) REFERENCES users (pk)
             );"""
    cursor.execute(sql)

    # Create the recipes table
    sql = """CREATE TABLE IF NOT EXISTS recipes (
             pk INT AUTO_INCREMENT PRIMARY KEY,
             id INT UNIQUE KEY,
             ingredients TEXT NOT NULL,
             recipe TEXT NOT NULL,
             nutrition_info TEXT NOT NULL,
             image LONGBLOB NOT NULL,
             prep_time INT NOT NULL
             );"""
    cursor.execute(sql)

    #Create meals table which uses recipes table to store the recipes locally
    sql = """CREATE TABLE IF NOT EXISTS meals (
             pk INT AUTO_INCREMENT PRIMARY KEY,
             plan_pk INT NOT NULL,
             meal VARCHAR(9) NOT NULL,
             time_served TIME NOT NULL,
             recipe_id INT NOT NULL,
             FOREIGN KEY (plan_pk) REFERENCES plans (pk),
             FOREIGN KEY (recipe_id) REFERENCES recipes (id));"""
    cursor.execute(sql)

if __name__ == "__main__":
    schema() 
