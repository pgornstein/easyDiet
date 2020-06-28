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

  useEffect(() => {
    async function redirect() {
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
      }
    }
  }
  redirect()
})
  
  const [today, setToday] = useState(new Date())

  //Override to return local time instead of UTC
  Date.prototype.toJSON = function(){ return moment(this).format(); }

  useEffect(() => {
    async function getTodaysMeals() {
      const formattedToday = today.toJSON().slice(0, 10);
      const data = {
        token: token,
        today: formattedToday
      }
      console.log(data)
      const configs = {
        method: "POST",
        mode: "cors",
        body: JSON.stringify(data),
        headers: {"Content-Type": "application/json"}
      }
      const response_package = await fetch("http://localhost:5000/get_todays_meals", configs)
      const response = await response_package.json()
      console.log(response)
    }
    getTodaysMeals()
  })
  return(null);
}