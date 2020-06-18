import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { MuiPickersUtilsProvider, DatePicker, TimePicker } from '@material-ui/pickers'
import DateFnsUtils from '@date-io/date-fns'
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

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
  if (date.getDate() != d) {
    date.setDate(0);
  }
  return date;
}

//Will set default times
const setTimes = () => {
  let a = new Date();
  let b = new Date();
  let c = new Date();
  a.setHours(7, 0, 0);
  b.setHours(12, 0, 0);
  c.setHours(19, 0, 0);
  return [a, b, c]
}

export default function Setup() {

  const [token, setToken] = useStateWithSessionStorage("token");
  const history = useHistory();

  const [breakfast, lunch, dinner] = setTimes();

  const [startDate, setStartDate] = useState(new Date())
  const [endDate, setEndDate] = useState(addMonth(new Date()))
  const [type, setType] = useState("")
  const [breakfastTime, setBreakfastTime] = useState(breakfast)
  const [lunchtime, setLunchtime] = useState(lunch)
  const [dinnertime, setDinnertime] = useState(dinner)
  const [calorieLimit, setCalorieLimit] = useState(0)

  const [requestSuccess, setRequestSuccess] = useState(true)

  const createDiet = async () => {
    const data = {
      token: token,
      startDate: startDate,
      endDate: endDate,
      type: type,
      breakfastTime: breakfastTime,
      lunchtime: lunchtime,
      dinnertime: dinnertime,
      calorieLimit: calorieLimit
    }
    console.log(data)
    const configs = {
      method: "POST",
      mode: "cors",
      body: JSON.stringify(data),
      headers: {"Content-Type": "application/json"}
    }
    const response_package = await fetch("http://localhost:5000/create_diet", configs)
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
              <FormControl className={classes.formControl}>
                <InputLabel id="diet_type_label">Diet</InputLabel>
                <Select
                  labelId="diet_type_label"
                  id="diet-type"
                  value={type}
                  onChange={setType}
                >
                  <MenuItem value="regular">Regular</MenuItem>
                  <MenuItem value="vegetarian">Vegetarian</MenuItem>
                  <MenuItem value="vegan">Vegan</MenuItem>
                  <MenuItem value="paleo">Pegan</MenuItem>
                </Select>
            </FormControl>
              <Grid item xs={12} sm={6}>
                <TimePicker value={breakfastTime} label="Breakfast time" onChange={setBreakfastTime} /> 
              </Grid>
              <Grid item xs={12} sm={6}>
                <TimePicker value={lunchtime} label="Lunchtime" onChange={setLunchtime} /> 
              </Grid>
              <Grid item xs={12} sm={6}>
                <TimePicker value={dinnertime} label="Dinnertime" onChange={setDinnertime} /> 
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className={classes.submit}
              onClick={e => {
                e.preventDefault()
                console.log(type)
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