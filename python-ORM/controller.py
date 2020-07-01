from flask import Flask, request, jsonify
from flask_cors import CORS
from user import User
from plan import Plan
from meal import Meal
from recipe import Recipe
from util import create_session, lookup_pk_by_session
from generate import generate_initial_meals

app = Flask(__name__)
CORS(app)

@app.route("/add_user", methods=["POST"])
def add_user():
    user_info = request.get_json()
    if user_info:
        if User.exists_user_with_email(user_info["email"]):
            return jsonify({"connected": True, "added": False})
        else:
            new_user = User(**user_info)
            new_user.save()
            return jsonify({"connected": True, "added": True})
    else:
        return jsonify({"connected": False})

@app.route("/login_user", methods=["POST"])
def login_user():
    user_info = request.get_json()
    if user_info:
        logged_in_user = User.login(user_info["email"], user_info["password"])
        if logged_in_user:
            token = create_session(logged_in_user.pk)
            return jsonify({"connected": True, "loggedIn": True, 
                             "token": token})
        else:
            return jsonify({"connected": True, "loggedIn": False})
    else:
        return jsonify({"connected": False})

@app.route("/create_plan", methods=["POST"])
def create_diet():
    success = True
    user_info = request.get_json()
    if user_info:
        user_pk = lookup_pk_by_session(user_info["token"])
        user_info["user_pk"] = user_pk
        new_plan = Plan(**user_info)
        new_plan.save()
        generate_initial_meals(user_pk)
    else:   
        success = False
    return jsonify({"success": success})

@app.route("/has_plan", methods=["POST"])
def has_plan():
    has = False
    success = True
    user_info = request.get_json()
    if user_info:
        user_pk = lookup_pk_by_session(user_info["token"])
        plan = Plan.plan_for_user(user_pk)
        if plan:
            has = True
    else:
        success = False
    return jsonify({"success": success, "hasPlan": has})

@app.route("/get_todays_meals", methods=["POST"])
def get_todays_meals():
    success = True
    result = {}
    user_info = request.get_json()
    if user_info:
        user_pk = lookup_pk_by_session(user_info["token"])
        plan = Plan.plan_for_user(user_pk)
        meals = plan.get_meals_for_day(user_info["today"])
        result["success"] = success
        for i in range(3):
            meal_result = {}
            meal = meals[i]
            recipe = meal.get_recipe()
            meal_result["time"] = str(meal.time_served)
            meal_result["name"] = meal.name
            meal_result["prepTime"] = recipe.prep_time
            meal_result["ingredients"] = recipe.ingredients
            meal_result["recipe"] = recipe.recipe
            meal_result["nutritionInfo"] = recipe.nutrition_info
            result[meal.meal] = meal_result # i.e. result["breakfast"] = meal_result
    else:
        success = False
    result["success"] = success
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)