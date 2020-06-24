import mysql.connector

class Recipe:

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.rid = kwargs.get("rid")
        self.ingredients = kwargs.get("ingredients")
        self.recipe = kwargs.get("recipe")
        self.nutrition_info = kwargs.get("nutrition_info")
        self.prep_time = kwargs.get("prep_time")

    def save(self):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = """INSERT INTO recipes (
                 rid, ingredients, recipe, nutrition_info, prep_time
                 ) VALUES (%s, %s, %s, %s, %s)"""
        values = (self.rid, self.ingredients, self.recipe, self.nutrition_info, 
                  self.prep_time)
        cursor.execute(sql, values)
        mydb.commit()

    def delete(self):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = "DELETE FROM recipes WHERE pk = %s"
        cursor.execute(sql, (self.pk,))
        mydb.commit()

    @classmethod
    def recipe_by_rid(cls, rid):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = "SELECT * FROM recipes WHERE rid = %s"
        cursor.execute(sql, (rid,))
        result = cursor.fetchone()
        if result:
            return cls(pk=result[0], rid=result[1], ingredients=result[2],
                       recipe=result[3], nutrition_info=result[4], prep_time=result[5])
        return None