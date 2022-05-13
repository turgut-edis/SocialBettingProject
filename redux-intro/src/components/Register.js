import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import "./csscomponents/components.css";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
    Switch,
   } from "react-router-dom";

export default function Register() {
  const [user, setUser] = useState("");
  const [pass, setPassword] = useState("");

  function validateForm() {
    return user.length > 0 && pass.length > 0;
  }

  function handleSubmit(event) {
    event.preventDefault();
  }

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
                <div class="bet-text2"><h3 class="text-whitesmoke">The best way to make bets while interacting with your friend!</h3></div>
                    
                <div class="container-content2">
                    <form >
                    <div class="group2"  >      
      <input type="text" class="input2" required/>
      <span class="highlight"></span>
      <span class="bar"></span>
      <label>First Name</label>
    </div>
      
    <div class="group2">      
      <input type="text" class="input2" required/>
      <span class="highlight"></span>
      <span class="bar"></span>
      <label>Last Name</label>
    </div>

    <div class="group2"  >      
      <input type="text" class="input2" required/>
      <span class="highlight"></span>
      <span class="bar"></span>
      <label>Pick a Username</label>
    </div>
      
    <div class="group3">      
      <label>Your Birthday :</label>
    </div>

    <div class="group4"  >      
<input type="date" name="dateofbirth" id="dateofbirth" class="input2"/>
    </div>

    <div class="group2"  >      
      <input type="text" class="input3" required/>
      <span class="highlight"></span>
      <span class="bar"></span>
      <label>Your Email Adress</label>
    </div>

    <div class="group2"  >      
      <input type="text" class="input2" required/>
      <span class="highlight"></span>
      <span class="bar"></span>
      <label>Pick a Password</label>
    </div>

    <div class="group2"  >      
      <input type="text" class="input2" required/>
      <span class="highlight"></span>
      <span class="bar"></span>
      <label>Retype your Password</label>
    </div>
                        <button type="submit" class="form-button button-l margin-b">Sign Up as Normal User</button>
                        <button type="submit" class="form-button button-l margin-b">Sign Up as Editor</button>
                  
                    </form>
                </div>
            </div>
</body>

  );
}