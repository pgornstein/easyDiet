import mysql.connector
from datetime import date, timedelta
import requests
from user import User
from plan import Plan
from meal import Meal
from recipe import Recipe

def generate_initial_meals(pk):
    user = User.user_for_pk(pk)
    plan = user.get_plan()
    start_date = plan.start_date
    end_date = plan.end_date
    difference = end_date - start_date
    days = difference.days + 1
    curr_date = start_date
    times = [plan.breakfast_time, plan.lunchtime, plan.dinnertime]
    if days > 30:
        days = 30
    for i in range(days):
        gen_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/mealplans/generate"
        if plan.type != "regular" :
            gen_querystring  = {"timeFrame": "day", "targetCalories": plan.calorie_limit,
                                "diet": plan.type}
        else:
            gen_querystring  = {"timeFrame": "day", "targetCalories": plan.calorie_limit}
        headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': "118c271f30mshaf7c7070fb3c9fdp1f7800jsn1dc535915371"
        }
        gen_response = requests.request("GET", gen_url, headers=headers, 
                                        params=gen_querystring)
        gen_data = gen_response.json()
        gen_meals = gen_data["meals"]
        for j in range(3):
            plan_pk = plan.pk
            name = gen_meals[j]["title"]
            meal = ""
            if j == 0:
                meal = "breakfast"
            elif j == 1:
                meal = "lunch"
            else:
                meal = "dinner"
            date_served = curr_date
            time_served = times[j]
            recipe_id = gen_meals[j]["id"]
            values = {"plan_pk": plan_pk, "name": name, "meal": meal, 
                      "date_served": date_served, "time_served": time_served,
                      "recipe_id": recipe_id}
            new_meal = Meal(**values)
            recipe = new_meal.get_recipe()
            if recipe is None:
                rid = recipe_id
                recipe_url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{rid}/information"
                recipe_querystring = {"includeNutrition":"true"}
                #reusing headers from before
                recipe_response = requests.request("GET", recipe_url, headers=headers, 
                                                   params=recipe_querystring)
                recipe_data = recipe_response.json()
                ingredients = ""
                for ingredient in recipe_data["extendedIngredients"]:
                    ingredients += ingredient["original"] + ', '
                recipe_recipe = recipe_data["instructions"]
                nutrition_info = ""
                nutrition_info += "Percent protein: " + str(recipe_data["nutrition"]["caloricBreakdown"]["percentProtein"]) + ', '
                nutrition_info += "Percent fat: " + str(recipe_data["nutrition"]["caloricBreakdown"]["percentFat"]) + ', '
                nutrition_info += "Percent carbs: " + str(recipe_data["nutrition"]["caloricBreakdown"]["percentCarbs"])
                prep_time = recipe_data["readyInMinutes"]
                values = {"rid": rid, "ingredients": ingredients, 
                          "recipe": recipe_recipe, "nutrition_info": nutrition_info,
                          "prep_time": prep_time}
                recipe = Recipe(**values)
                recipe.save()
            new_meal.save()
        add_day = timedelta(days=1)
        curr_date = curr_date + add_day

if __name__ == "__main__":
    generate_initial_meals(4)
