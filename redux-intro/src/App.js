import React from 'react';
import './App.css';
import Counter from "./components/Counter"
import IncreaseCounter from "./components/IncreaseCounter"
import DecreaseCounter from "./components/DecreaseCounter"
import IncreaseByTwoCounter from "./components/IncreaseByTwoCounter"
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';

import Login from "./components/Login";
import Register from "./components/Register";
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
  <nav className="navbar navbar-expand-lg navbar-light fixed-top">
      <div className="container">
        <Link className="navbar-brand" to={"/"}>BETaBET</Link>
        <div className="collapse navbar-collapse" id="navbarTogglerDemo02">
          <ul className="navbar-nav ml-auto">
            <li className="nav-item">
              <Link className="nav-link" to={"/"}>Login</Link>
            </li>
            <li className="nav-item2">
              <Link className="nav-link" to={"/register"}>Register</Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    
    <div className="outer">
      <div className="inner">
      <Routes>
      <Route path="/" element={<Login/>} />
      <Route path="/register" element={<Register/>} />
      </Routes>
      </div>
    </div>
    </div>
   
  </Router>



  );
}

export default App;
