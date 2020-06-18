import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import Login from './Login';
import Register from './Register'
import Setup from './Setup'
import Calendar from './Calendar'

const Router = () => {
  return(
    <div>
      <Route path="/login" component={Login} />
      <Route path="/register" component={Register} />
      <Route path="/setup" component={Setup} />
      <Route path="/calendar" component={Calendar} />
      <Redirect from="/" to="/login" />
    </div>
  )
}

export default Router;