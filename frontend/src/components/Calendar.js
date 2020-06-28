import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import moment from 'moment'

const useStateWithSessionStorage = (key) => {
  const [data, setData] = useState(sessionStorage.getItem(key) || "");
  return [data, setData]
}

export default function Calendar() {

  const [token, setToken] = useStateWithSessionStorage("token");
  const history = useHistory();

  const [today, setToday] = useState(new Date())
  
  const [breakfastTime, setBreakfastTime] = useState("")
  const [breakfastName, setBreakfastName] = useState("")
  const [breakfastPrepTime, setBreakfastPrepTime] = useState("")
  const [breakfastIngredients, setBreakfastIngredients] = useState("")
  const [breakfastRecipe, setBreakfastRecipe] = useState("")
  const [breakfastNutrition, setBreakfastNutrition] = useState("")

  const [lunchtime, setLunchtime] = useState("")
  const [lunchName, setLunchName] = useState("")
  const [lunchPrepTime, setLunchPrepTime] = useState("")
  const [lunchIngredients, setLunchIngredients] = useState("")
  const [lunchRecipe, setLunchRecipe] = useState("")
  const [lunchNutrition, setLunchNutrition] = useState("")

  const [dinnertime, setDinnertime] = useState("")
  const [dinnerName, setDinnerName] = useState("")
  const [dinnerPrepTime, setDinnerPrepTime] = useState("")
  const [dinnerIngredients, setDinnerIngredients] = useState("")
  const [dinnerRecipe, setDinnerRecipe] = useState("")
  const [dinnerNutrition, setDinnerNutrition] = useState("")

  //Override to return local time instead of UTC
  Date.prototype.toJSON = function(){ return moment(this).format(); }

  useEffect(() => {
    async function eventHandler() {
    if (token === "") {
      history.push("/login")
    } else {
      const data = {token: token};
      const configs = {
        method: "POST",
        mode: "cors",
        body: JSON.stringify(data),
        headers: {"Content-Type": "application/json"}
      }
      const response_package = await fetch("http://localhost:5000/has_plan", configs)
      const response = await response_package.json()
      console.log(response)
      if (response.success && !(response.hasPlan)) {
        history.push("/setup")
      } else {
        const formattedToday = today.toJSON().slice(0, 10);
        const data2 = {
          token: token,
          today: formattedToday
        }
        console.log(data2)
        const configs = {
          method: "POST",
          mode: "cors",
          body: JSON.stringify(data2),
          headers: {"Content-Type": "application/json"}
        }
        const response_package2 = await fetch("http://localhost:5000/get_todays_meals", configs)
        const response2 = await response_package2.json()
        console.log(response2)
        if (response2.success) {
          setBreakfastTime(response2.breakfast.time)
          setBreakfastName(response2.breakfast.name)
          setBreakfastPrepTime(response2.breakfast.prepTime)
          setBreakfastIngredients(response2.breakfast.ingredients)
          setBreakfastRecipe(response2.breakfast.recipe)
          setBreakfastNutrition(response2.breakfast.nutritionInfo)

          setLunchtime(response2.lunch.time)
          setLunchName(response2.lunch.name)
          setLunchPrepTime(response2.lunch.prepTime)
          setLunchIngredients(response2.lunch.ingredients)
          setLunchRecipe(response2.lunch.recipe)
          setLunchNutrition(response2.lunch.nutritionInfo)
          
          setDinnertime(response2.dinner.time)
          setDinnerName(response2.dinner.name)
          setDinnerPrepTime(response2.dinner.prepTime)
          setDinnerIngredients(response2.dinner.ingredients)
          setDinnerRecipe(response2.dinner.recipe)
          setDinnerNutrition(response2.dinner.nutritionInfo)
        }
      }
    }
  }
  eventHandler()
}, [])

  return(
    <div>
      <h1>Hello</h1>
    </div>
  );
}