import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import "./csscomponents/components.css";
import { useNavigate } from 'react-router-dom';
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
    Switch,
   } from "react-router-dom";

export default function Login() {
  const [user, setUser] = useState("");
  const [pass, setPassword] = useState("");
  const navigate = useNavigate();

  function validateForm() {
    return user.length > 0 && pass.length > 0;
  }
  const handleSubmit = async (e) => {
    e.preventDefault();
    navigate('/homepage');
  };

  return (
    <body>
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
        <div class="login-container text-c animated flipInX">
                <div>
                    <h1 class="logo-badge text-whitesmoke"><span class="fa fa-user-circle"></span></h1>
                </div>
                <div class="bet-text"><h3 class="text-whitesmoke">The best way to make bets while interacting with your friend!</h3></div>
                    
                <div class="container-content">
            
                    <form class="margin-t" onSubmit={handleSubmit}>
                    <div class="group">      
      <input type="user" required/>
      <span class="highlight"></span>
      <span class="bar"></span>
      <label>Name</label>
    </div>
      
    <div class="group">      
      <input type="password"  id="myInput" required/>
      <span class="highlight"></span>
      <span class="bar"></span>
      <label>Password</label>
    </div>
                        <button type="submit" class="form-button button-l margin-b">Sign In</button>
                        <a class="text-darkyellow" href="#"><small>Forgot your password?</small></a>
                        <p class="text-whitesmoke text-center"><small>Do not have an account?</small></p>
                        <a class="text-darkyellow" href="#"><small>Sign Up</small></a>
                    </form>
                </div>
            </div>
</body>

  );
}