import mysql.connector
from meal import Meal

class Plan:

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.user_pk = kwargs.get("user_pk")
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.type = kwargs.get("type")
        self.breakfast_time = kwargs.get("breakfast_time")
        self.lunchtime = kwargs.get("lunchtime")
        self.dinnertime = kwargs.get("dinnertime")
        self.calorie_limit = kwargs.get("calorie_limit")

    def save(self):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = """INSERT INTO plans (
                 user_pk, start_date, end_date, type, breakfast_time, lunchtime, 
                 dinnertime, calorie_limit
                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (self.user_pk, self.start_date, self.end_date, self.type, 
                  self.breakfast_time, self.lunchtime, self.dinnertime,
                  self.calorie_limit)
        cursor.execute(sql, values)
        mydb.commit()

    def delete(self):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = "DELETE FROM plans WHERE pk = %s"
        cursor.execute(sql, (self.pk,))
        mydb.commit()

    @classmethod
    def plan_for_user(cls, user_pk):
        mydb = mysql.connector.connect(user='easyDiet', password='diet/SMART2020',
                                       host='127.0.0.1', database='diet')
        cursor = mydb.cursor()
        sql = "SELECT * FROM plans WHERE user_pk = %s"
        cursor.execute(sql, (user_pk,))
        result = cursor.fetchone()
        if result:
            return cls(pk=result[0], user_pk=result[1], start_date=result[2], 
                       end_date=result[3], type=result[4], breakfast_time=result[5], 
                       lunchtime=result[6], dinnertime=result[7], 
                       calorie_limit=result[8])
        return None

    def get_all_meals(self):
        meals = Meal.meals_for_plan(self.pk)
        return meals

    def get_meals_for_day(self, date):
        meals = Meal.meals_by_day(self.pk, date)
        return meals