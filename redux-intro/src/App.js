import React from 'react';
import './App.css';
import Counter from "./components/Counter"
import IncreaseCounter from "./components/IncreaseCounter"
import DecreaseCounter from "./components/DecreaseCounter"
import IncreaseByTwoCounter from "./components/IncreaseByTwoCounter"
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';

import Login from "./components/Login";
import Register from "./components/Register";
import HomePage from './components/HomePage';

import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Switch,
 } from "react-router-dom";

 const App = () => {
  return (
    

  <Router>
  
   
    <div className="App">
    <div className="outer">
      <div className="inner">
      <Routes>
      <Route path="/" element={<Login/>} />
      <Route path="/register" element={<Register/>} />
      <Route path="/homepage" element={<HomePage/>} />
      </Routes>
      </div>
    </div>
    </div>
   
  </Router>



  );
}

export default App;
