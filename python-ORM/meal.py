import mysql.connector
from recipe import Recipe

class Meal:

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.plan_pk = kwargs.get("plan_pk")
        self.name = kwargs.get("name")
        self.meal = kwargs.get("meal")
        self.date_served = kwargs.get("date_served")
        self.time_served = kwargs.get("time_served")
        self.recipe_id = kwargs.get("recipe_id")

    def save(self):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = """INSERT INTO meals (
                 plan_pk, name, meal, date_served, time_served, recipe_id
                 ) VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (self.plan_pk, self.name, self.meal, self.date_served, self.time_served, 
                  self.recipe_id)
        cursor.execute(sql, values)
        mydb.commit()

    def delete(self):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = "DELETE FROM meals WHERE pk = %s"
        cursor.execute(sql, (self.pk,))
        mydb.commit()

    @classmethod
    def meals_for_plan(cls, plan_pk):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = "SELECT * FROM meals WHERE plan_pk = %s"
        cursor.execute(sql, (plan_pk,))
        generated_result = cursor.fetchall()
        if generated_result:
            result = []
            for meal in generated_result:
                newMeal = cls(pk=meal[0], plan_pk=meal[1], name=meal[2],
                              meal=meal[3], date_served=meal[4], 
                              time_served=meal[5], recipe_id=meal[6])
                result.append(newMeal)
            return result
        return None

    @classmethod
    def meals_by_day(cls, plan_pk, date_served):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = """SELECT * 
                 FROM meals 
                 WHERE plan_pk = %s AND date_served = %s
                 ORDER BY time_served"""
        cursor.execute(sql, (plan_pk, date_served))
        generated_result = cursor.fetchall()
        if generated_result:
            result = []
            for meal in generated_result:
                newMeal = cls(pk=meal[0], plan_pk=meal[1], name=meal[2],
                              meal=meal[3], date_served=meal[4], 
                              time_served=meal[5], recipe_id=meal[6])
                result.append(newMeal)
            return result
        return None

    def get_recipe(self):
        recipe = Recipe.recipe_by_rid(self.recipe_id)
        return recipe