import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { MuiPickersUtilsProvider, DatePicker, TimePicker } from '@material-ui/pickers'
import DateFnsUtils from '@date-io/date-fns'
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import NumericInput from 'react-numeric-input';
import moment from 'moment'

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(3),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

const useStateWithSessionStorage = (key) => {
  const [data, setData] = useState(sessionStorage.getItem(key) || "");
  return [data, setData]
}

//Function will be used to get date a month from now 
const addMonth = (date) => {
  const d = date.getDate();
  date.setMonth(date.getMonth() + 1);
  if (date.getDate() !== d) {
    date.setDate(0);
  }
  return date;
}

//Will set default times
const setTimes = () => {
  let a = new Date();
  let b = new Date();
  let c = new Date();
  //Times adjusted so that GMT looks like our local time
  a.setHours(7, 0, 0);
  b.setHours(12, 0, 0);
  c.setHours(19, 0, 0);
  return [a, b, c]
}

export default function Setup() {

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
      if (response.success && response.hasPlan) {
        history.push("/calendar")
      }
    }
  }
  redirect()
})

  const [breakfast, lunch, dinner] = setTimes();

  const [startDate, setStartDate] = useState(new Date())
  const [endDate, setEndDate] = useState(addMonth(new Date()))
  const [type, setType] = useState("regular")
  const [breakfastTime, setBreakfastTime] = useState(breakfast)
  const [lunchtime, setLunchtime] = useState(lunch)
  const [dinnertime, setDinnertime] = useState(dinner)
  const [calorieLimit, setCalorieLimit] = useState(2000)

  const [requestSuccess, setRequestSuccess] = useState(true)

  //Override to return local time instead of UTC
  Date.prototype.toJSON = function(){ return moment(this).format(); }

  const createDiet = async () => {
    const formattedStartDate = startDate.toJSON().slice(0, 10);
    const formattedEndDate = endDate.toJSON().slice(0, 10);
    const formattedBreakfastTime = breakfastTime.toJSON().slice(11, 19);
    const formattedLunchtime = lunchtime.toJSON().slice(11, 19);
    const formattedDinnertime = dinnertime.toJSON().slice(11, 19);
    const data = {
      token: token,
      start_date: formattedStartDate,
      end_date: formattedEndDate,
      type: type,
      breakfast_time: formattedBreakfastTime,
      lunchtime: formattedLunchtime,
      dinnertime: formattedDinnertime,
      calorie_limit: calorieLimit
    }
    console.log(data)
    const configs = {
      method: "POST",
      mode: "cors",
      body: JSON.stringify(data),
      headers: {"Content-Type": "application/json"}
    }
    const response_package = await fetch("http://localhost:5000/create_plan", configs)
    const response = await response_package.json()
    console.log(response)
    setRequestSuccess(response.success)
    if (requestSuccess) {
      history.push("/calendar")
    }
  }

  const classes = useStyles();
  
  return (

    <MuiPickersUtilsProvider utils={DateFnsUtils}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <div className={classes.paper} style={{textAlign: "center"}}>
          <Avatar className={classes.avatar}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5" style={{textAlign: "left"}}>
            Sign up
          </Typography>
          <form className={classes.form} noValidate>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <DatePicker value={startDate} label="Start Date" onChange={setStartDate} /> 
              </Grid>
              <Grid item xs={12} sm={6}>
              <DatePicker value={endDate} label="End Date" onChange={setEndDate} /> 
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl className={classes.formControl}>
                  <InputLabel id="diet_type_label">Diet</InputLabel>
                  <Select
                    labelId="diet_type_label"
                    id="diet-type"
                    value={type}
                    onChange={e => setType(e.target.value)}
                  >
                    <MenuItem value="regular">Regular</MenuItem>
                    <MenuItem value="vegetarian">Vegetarian</MenuItem>
                    <MenuItem value="vegan">Vegan</MenuItem>
                    <MenuItem value="paleo">Paleo</MenuItem>
                  </Select>
              </FormControl>
            </Grid>
              <Grid item xs={12} sm={6}>
                <TimePicker value={breakfastTime} label="Breakfast time" onChange={setBreakfastTime} /> 
              </Grid>
              <Grid item xs={12} sm={6}>
                <TimePicker value={lunchtime} label="Lunchtime" onChange={setLunchtime} /> 
              </Grid>
              <Grid item xs={12} sm={6}>
                <TimePicker value={dinnertime} label="Dinnertime" onChange={setDinnertime} /> 
              </Grid>
              <Grid item xs={12} sm={6}>
                <label>Calorie limit</label>
                <NumericInput min={0} max={10000} value={calorieLimit} step={20}
                              onChange={e => setCalorieLimit(e)} />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className={classes.submit}
              onClick={e => {
                e.preventDefault();
                createDiet();
              }}
            >
              Sign Up
            </Button>
          </form>
        </div>
      </Container>
    </MuiPickersUtilsProvider>
  );
}