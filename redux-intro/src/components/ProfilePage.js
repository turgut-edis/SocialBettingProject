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

export default function ProfilePage() {
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
      <div className="container">
      <nav className="navbar navbar-expand-lg navbar-light fixed-top">
        <Link className="navbar-brand" to={"/"}>BETaBET</Link>
        <div className="collapse navbar-collapse" id="navbarTogglerDemo02">
          <ul className="navbar-nav ml-auto">
          <li className="nav-item3">
              <Link className="nav-link" to={"/homepage"}>Home</Link>
            </li>
            <li className="nav-item4">
              <Link className="nav-link" to={"/socialpage"}>Social</Link>
            </li>
            <li className="nav-item5">
              <Link className="nav-link" to={"/profilepage"}>Profile</Link>
            </li>
            <li className="nav-item6">
              <Link className="nav-link" to={"/raffle"}>Raffle</Link>
            </li>
            <li className="nav-item9">
            <button type="button" class="btn btn-light">Edit</button>
            </li>
            <br></br>
            <li className="nav-item10">
            <p >Name Balance</p>
            </li>
            <br></br>
            <li className="nav-item8">
            <button type="button" class="btn btn-light">Change Balance</button>
            </li>
            
            <li className="nav-item2">
              <Link className="nav-link" to={"/"}>Logout</Link>
            </li>
          </ul>
        </div>
        </nav>
        <div id="cover">
  <form method="get" action="" class="form2">
    <div class="tb">
      <div class="td"><input type="text" placeholder="Search" required/></div>
      <div class="td" id="s-cover">
        <button type="submit" class="button2">
          <div id="s-circle"></div>
          <span></span>
        </button>
      </div>
    </div>
  </form>
  <div class="left-rect10">
  <button type="button" class="btn btn-danger btn-lg" >Add Friend</button>

  </div>
</div>
<div class="right-rect10">Finished Slips</div>
<div class="right-rect11">Unfinished Slips</div>
<div class="right-rect12">Friends List</div>
<div class="right-rect13">Purchased Tickets</div>
      </div>
</body>

  );
}