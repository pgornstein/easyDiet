import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  }
}));

const NavBar = () => {

  return (
    <nav style={{textAlign: "center"}}>
      <Button color="inherit"component={Link} to={'/login'}>Login</Button>
      <Button color="inherit"component={Link} to={'/register'}>Register</Button>
      <Button color="inherit"component={Link} to={'/setup'}>Setup</Button>
      <Button color="inherit"component={Link} to={'/calendar'}>Calendar</Button>
      <Button color="inherit"component={Link}to={'/login'}
      onClick={e => sessionStorage.setItem("token", "")}>Logout</Button>
    </nav>
  )
}

export default NavBar;