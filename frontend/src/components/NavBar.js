import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = () => {
  return (
    <nav style={{textAlign: "center"}}>
      <Link to="/login">Log In</Link>
      <Link to="/register">Register</Link>
      <Link to="/setup">Setup</Link>
      <Link to="/calendar">Calendar</Link>
    </nav>
  )
}

export default NavBar;