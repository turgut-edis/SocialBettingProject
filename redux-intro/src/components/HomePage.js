import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import logo from './image/clipart442066.png'
import "./csscomponents/components.css";

import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
    Switch,
   } from "react-router-dom";

export default function HomePage() {
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
            <li className="nav-item8">
              <p>Funds:1500 TRY {user}</p>
            </li>
            <li className="nav-item7">
              <p>Welcome, {user}</p>
            </li>
            <li className="nav-item2">
              <Link className="nav-link" to={"/"}>Logout</Link>
            </li>
          </ul>
        </div>
        </nav>
      </div>
    
  
    <div class="right-rect">
        My Betslips
    </div>
    <div class="right-rect2">
    <img src={logo} className="logo" alt="logo" />
        Galatasaray - Real Madrid 
        <div class= "txtforball">2</div>
        <div class="txtforball2">MS:2 Odd:2.5</div>
        
    </div>
    <div class="right-rect3">
    <img src={logo} className="logo" alt="logo" />
    Fenerbahçe - Beşiktaş 
        <div class= "txtforball">5</div>
        <div class="txtforball2">FH/MR: 0/X RC:2</div>
        <div class="txtforball3">Odd: 11.9</div>
    </div>
    
    
    <div class="left-rect">
    <nav class="navHomeTable">
	<a href="#all">All</a>
	<a href="#football">Football</a>
	<a href="#basketball">Basketball</a>
	<a href="#tennis">Tennis</a>
	<a href="#contact">Contact</a>
	<div class="animation start-home"></div>
</nav>

        <div class="navt">UEFA Champions League</div>
        
        
        
        <table id="all" class="table table-striped table-bordered table-sm " cellspacing="0"
  width="100%">
  <thead>
 
    <tr>
      <th>First name</th>
      <th>Last name</th>
      <th>Position</th>
      <th>Office</th>
      <th>Age</th>
      <th>Start date</th>
      <th>Salary</th>
      <th>Extn.</th>
      <th>E-mail</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Tiger</td>
      <td>Nixon</td>
      <td>System Architect</td>
      <td>Edinburgh</td>
      <td>61</td>
      <td>2011/04/25</td>
      <td>$320,800</td>
      <td>5421</td>
      <td>t.nixon@datatables.net</td>
    </tr>
    <tr>
      <td>Garrett</td>
      <td>Winters</td>
      <td>Accountant</td>
      <td>Tokyo</td>
      <td>63</td>
      <td>2011/07/25</td>
      <td>$170,750</td>
      <td>8422</td>
      <td>g.winters@datatables.net</td>
    </tr>
    <tr>
      <td>Ashton</td>
      <td>Cox</td>
      <td>Junior Technical Author</td>
      <td>San Francisco</td>
      <td>66</td>
      <td>2009/01/12</td>
      <td>$86,000</td>
      <td>1562</td>
      <td>a.cox@datatables.net</td>
    </tr>
    <tr>
      <td>Cedric</td>
      <td>Kelly</td>
      <td>Senior Javascript Developer</td>
      <td>Edinburgh</td>
      <td>22</td>
      <td>2012/03/29</td>
      <td>$433,060</td>
      <td>6224</td>
      <td>c.kelly@datatables.net</td>
    </tr>
    <tr>
      <td>Airi</td>
      <td>Satou</td>
      <td>Accountant</td>
      <td>Tokyo</td>
      <td>33</td>
      <td>2008/11/28</td>
      <td>$162,700</td>
      <td>5407</td>
      <td>a.satou@datatables.net</td>
    </tr>
    <tr>
      <td>Brielle</td>
      <td>Williamson</td>
      <td>Integration Specialist</td>
      <td>New York</td>
      <td>61</td>
      <td>2012/12/02</td>
      <td>$372,000</td>
      <td>4804</td>
      <td>b.williamson@datatables.net</td>
    </tr>
  </tbody>
</table>

    </div>
    
</body>

  );
}