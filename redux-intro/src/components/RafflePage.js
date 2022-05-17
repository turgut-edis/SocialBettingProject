import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import "./csscomponents/components.css";
import logo from './image/clipart442066.png'
import trash_icon from './image/trash-347.png'
import raffle_ticket from './image/raffle-ticket.png'


import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Switch,
} from "react-router-dom";
import { Card, CardGroup, Tab, Tabs } from "react-bootstrap";


var cart_total = 160;
var item = "Banana Mairpods"
var price = 80;
var product_name = "Banana Mairpods MAX"
var date = "17/05/2022"

export default function RafflePage() {
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
        <div className="raffle-container">
          <div className="raffle-content">
            <CardGroup className="raffle-cards">
            <div>
            <Card style={{ width: '20rem', height: '20rem', marginRight:'3rem'}} className="raffle_card">
              <Card.Img variant="top" src={raffle_ticket} className="raffle_img"/>
              <Card.Body>
                <Card.Title className="raffle-name">{item}</Card.Title>
                <h6 className="raffle-price">TRY {price}</h6>
                <h6 className="raffle-date">{date}</h6>
                <Button variant="primary" className="raffle-button">Buy Ticket</Button>
              </Card.Body>
            </Card>
            </div>
            <div>
            <Card style={{ width: '20rem', height: '20rem', marginRight:'3rem'}} className="raffle_card">
              <Card.Img variant="top" src={raffle_ticket} className="raffle_img"/>
              <Card.Body>
                <Card.Title className="raffle-name">{product_name}</Card.Title>
                <h6 className="raffle-price">TRY {price}</h6>
                <h6 className="raffle-date">{date}</h6>
                <Button variant="primary" className="raffle-button">Buy Ticket</Button>
              </Card.Body>
            </Card>
            </div>  
            <div>
            <Card style={{ width: '20rem', height: '20rem', marginRight:'3rem'}} className="raffle_card">
              <Card.Img variant="top" src={raffle_ticket} className="raffle_img"/>
              <Card.Body>
                <Card.Title className="raffle-name">{product_name}</Card.Title>
                <h6 className="raffle-price">TRY {price}</h6>
                <h6 className="raffle-date">{date}</h6>
                <Button variant="primary" className="raffle-button">Buy Ticket</Button>
              </Card.Body>
            </Card>
            </div>  
            <div>
            <Card style={{ width: '20rem', height: '20rem', marginRight:'3rem'}} className="raffle_card">
              <Card.Img variant="top" src={raffle_ticket} className="raffle_img"/>
              <Card.Body>
                <Card.Title className="raffle-name">{product_name}</Card.Title>
                <h6 className="raffle-price">TRY {price}</h6>
                <h6 className="raffle-date">{date}</h6>
                <Button variant="primary" className="raffle-button">Buy Ticket</Button>
              </Card.Body>
            </Card>
            </div>   
            </CardGroup>
          </div>
          <div className="raffle-cart">
            <CardGroup>
              <Card>
                <Card.Header as="h5">My Cart</Card.Header>
                <Card.Body>
                  <div className="rightpanel-betslip">
                    <h6><img src={raffle_ticket} className="raffle-logo" alt="ticket" /><span> {item} MAX </span></h6>
                    <h6 className="raffle-info">TRY {price}</h6>
                  </div>
                </Card.Body>
              </Card>
            </CardGroup>
            <Card>
              <Card.Body>
                <div className="rightpanel-betslip">
                  <h6><img src={raffle_ticket} className="raffle-logo" alt="ticket" /><span> {item} </span></h6>
                  <h6 className="raffle-info">TRY {price}</h6>
                </div>
              </Card.Body>
            </Card>
            <div className="raffle-checkout-card">
              <Card>
                <Card.Body>
                  <div className="rightpanel-checkout">
                    <h6 className="checkout">Cart Total: TRY{cart_total}</h6>
                  </div>
                  <div>
                    <img src={trash_icon} className="lower-icon" alt="delete" onclick="trash()" />
                    <Button variant="success" className="checkout-button" onclick="place_bet(amount_bet)">Buy Tickets</Button>
                  </div>
                </Card.Body>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </body>

  );
}