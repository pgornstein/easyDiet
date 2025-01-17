import React from 'react';
import { BrowserRouter } from 'react-router-dom'
import logo from './logo.svg';
import './App.css';
import NavBar from './components/NavBar'
import Router from './components/Router'

function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <Router />
    </BrowserRouter>
  );
}

export default App;
