import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import "./csscomponents/LogReg.css";

export default function Login() {
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
        <div class="login-container text-c animated flipInX">
                <div>
                    <h1 class="logo-badge text-whitesmoke"><span class="fa fa-user-circle"></span></h1>
                </div>
                <div class="bet-text"><h3 class="text-whitesmoke">The best way to make bets while interacting with your friend!</h3></div>
                    
                <div class="container-content">
                    <form class="margin-t">
                    <div class="group">      
      <input type="text" required/>
      <span class="highlight"></span>
      <span class="bar"></span>
      <label>Name</label>
    </div>
      
    <div class="group">      
      <input type="text" required/>
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