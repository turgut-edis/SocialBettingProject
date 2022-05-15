import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Tabs from 'react-bootstrap/Tabs'
import "./csscomponents/components.css";
import userpic from './image/userpic.png'
import logo from './image/clipart442066.png'
import like_icon from './image/like-button.png'

import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Switch,
} from "react-router-dom";
import { Card, CardGroup, Tab } from "react-bootstrap";

var text = "Curated Editors\n";
var username = "Dodo";
var likecnt = "10";
var team1 = "Team1";
var team2 = "Team2";
var mac_sonu = "2";
var odd = "2.55";
var mac_id = "5";
var shared_match_cnt = "2";
var shared_slip_total_odd = "90.00";

export default function SocialPage() {
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
      <div className="social-container">
        <div className="social-card">

          <CardGroup>
            <Card border="primary" style={{ height: '25rem' }}>
              <Card.Header as="h5">{text}</Card.Header>
              <Card.Body>
                <Card.Title>I'm sharing this betslip for your use guyzz!!</Card.Title>
                <Card.Text as="h6">
                  <img src={userpic} className="user-picture" alt="user" />
                  <a>  {username}</a>
                  <img src={like_icon} className="like-pic" alt="likebtn" />
                  <a>  {likecnt}</a>
                  <Button variant="primary" className="betslip-use">Use This Betslip</Button>
                  <p> </p>
                  <div className="shared-betslip">
                    <img src={logo} className="ball-logo" alt="ball" />
                    <a> {team1} - {team2} </a>
                    <h6 className="mac_id_spacing">{mac_id} 
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                  <div className="shared-betslip">
                    <img src={logo} className="ball-logo" alt="ball" />
                    <a> {team1} - {team2} </a>
                    <h6 className="mac_id_spacing">{mac_id} 
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                  <div className="shared-betslip-stat">
                    <p></p>
                    <p className="shared-betslip-tot-match">Total Matches</p>
                    <p className="shared-betslip-tot-match-cnt">{shared_match_cnt}</p>
                    <p></p>
                    <p className="shared-betslip-tot-match">Total Odd</p>
                    <p className="shared-betslip-tot-match-cnt">{shared_slip_total_odd}</p>
                  </div>

                </Card.Text>
              </Card.Body>
            </Card>
            <Card border="primary" style={{ height: '25rem' }}>
              <Card.Header as="h5">Friends</Card.Header>
              <Card.Body>
                <Card.Title>Special title treatment</Card.Title>
                <Card.Text as="h6">
                  <img src={userpic} className="user-picture" alt="user" />
                  <a>  {username}</a>
                  <img src={like_icon} className="like-pic" alt="likebtn" />
                  <a>  {likecnt}</a>
                  <Button variant="primary" className="betslip-use">Use This Betslip</Button>
                  <p> </p>
                  <div className="shared-betslip">
                    <img src={logo} className="ball-logo" alt="ball" />
                    <a> {team1} - {team2} </a>
                    <h6 className="mac_id_spacing">{mac_id} 
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                  <div className="shared-betslip">
                    <img src={logo} className="ball-logo" alt="ball" />
                    <a> {team1} - {team2} </a>
                    <h6 className="mac_id_spacing">{mac_id} 
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                  <div className="shared-betslip-stat">
                    <p></p>
                    <p className="shared-betslip-tot-match">Total Matches</p>
                    <p className="shared-betslip-tot-match-cnt">{shared_match_cnt}</p>
                    <p></p>
                    <p className="shared-betslip-tot-match">Total Odd</p>
                    <p className="shared-betslip-tot-match-cnt">{shared_slip_total_odd}</p>
                  </div>

                </Card.Text>
              </Card.Body>
            </Card>
          </CardGroup>
          <CardGroup>
            <Card border="primary" style={{ height: '25rem' }}>
              <Card.Body>
                <Card.Title>Special title treatment</Card.Title>
                <Card.Text as="h6">
                  <img src={userpic} className="user-picture" alt="user" />
                  <a>  {username}</a>
                  <img src={like_icon} className="like-pic" alt="likebtn" />
                  <a>  {likecnt}</a>
                  <Button variant="primary" className="betslip-use">Use This Betslip</Button>
                  <p> </p>
                  <div className="shared-betslip">
                    <img src={logo} className="ball-logo" alt="ball" />
                    <a> {team1} - {team2} </a>
                    <h6 className="mac_id_spacing">{mac_id} 
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                  <div className="shared-betslip">
                    <img src={logo} className="ball-logo" alt="ball" />
                    <a> {team1} - {team2} </a>
                    <h6 className="mac_id_spacing">{mac_id} 
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                  <div className="shared-betslip-stat">
                    <p></p>
                    <p className="shared-betslip-tot-match">Total Matches</p>
                    <p className="shared-betslip-tot-match-cnt">{shared_match_cnt}</p>
                    <p></p>
                    <p className="shared-betslip-tot-match">Total Odd</p>
                    <p className="shared-betslip-tot-match-cnt">{shared_slip_total_odd}</p>
                  </div>

                </Card.Text>
              </Card.Body>
            </Card>
            <Card border="primary" style={{ height: '25rem' }}>
              <Card.Body>
                <Card.Title>Special title treatment</Card.Title>
                <Card.Text as="h6">
                  <img src={userpic} className="user-picture" alt="user" />
                  <a>  {username}</a>
                  <img src={like_icon} className="like-pic" alt="likebtn" />
                  <a>  {likecnt}</a>
                  <Button variant="primary" className="betslip-use">Use This Betslip</Button>
                  <p> </p>
                  <div className="shared-betslip">
                    <img src={logo} className="ball-logo" alt="ball" />
                    <a> {team1} - {team2} </a>
                    <h6 className="mac_id_spacing">{mac_id} 
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                  <div className="shared-betslip">
                    <img src={logo} className="ball-logo" alt="ball" />
                    <a> {team1} - {team2} </a>
                    <h6 className="mac_id_spacing">{mac_id} 
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                  <div className="shared-betslip-stat">
                    <p></p>
                    <p className="shared-betslip-tot-match">Total Matches</p>
                    <p className="shared-betslip-tot-match-cnt">{shared_match_cnt}</p>
                    <p></p>
                    <p className="shared-betslip-tot-match">Total Odd</p>
                    <p className="shared-betslip-tot-match-cnt">{shared_slip_total_odd}</p>
                  </div>

                </Card.Text>
              </Card.Body>
            </Card>
          </CardGroup>
          <CardGroup>
            <Card border="primary" style={{ height: '25rem' }}>
              <Card.Body>
                <Card.Title>Special title treatment</Card.Title>
                <Card.Text as="h6">
                  <img src={userpic} className="user-picture" alt="user" />
                  <a>  {username}</a>
                  <img src={like_icon} className="like-pic" alt="likebtn" />
                  <a>  {likecnt}</a>
                  <Button variant="primary" className="betslip-use">Use This Betslip</Button>
                  <p> </p>
                  <div className="shared-betslip">
                    <img src={logo} className="ball-logo" alt="ball" />
                    <a> {team1} - {team2} </a>
                    <h6 className="mac_id_spacing">{mac_id} 
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                  <div className="shared-betslip">
                    <img src={logo} className="ball-logo" alt="ball" />
                    <a> {team1} - {team2} </a>
                    <h6 className="mac_id_spacing">{mac_id} 
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                  <div className="shared-betslip-stat">
                    <p></p>
                    <p className="shared-betslip-tot-match">Total Matches</p>
                    <p className="shared-betslip-tot-match-cnt">{shared_match_cnt}</p>
                    <p></p>
                    <p className="shared-betslip-tot-match">Total Odd</p>
                    <p className="shared-betslip-tot-match-cnt">{shared_slip_total_odd}</p>
                  </div>

                </Card.Text>
              </Card.Body>
            </Card>
            <Card border="primary" style={{ height: '25rem' }}>
              <Card.Body>
                <Card.Title>Special title treatment</Card.Title>
                <Card.Text as="h6">
                  <img src={userpic} className="user-picture" alt="user" />
                  <a>  {username}</a>
                  <img src={like_icon} className="like-pic" alt="likebtn" />
                  <a>  {likecnt}</a>
                  <Button variant="primary" className="betslip-use">Use This Betslip</Button>
                  <p> </p>
                  <div className="shared-betslip">
                    <img src={logo} className="ball-logo" alt="ball" />
                    <a> {team1} - {team2} </a>
                    <h6 className="mac_id_spacing">{mac_id} 
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                  <div className="shared-betslip">
                    <img src={logo} className="ball-logo" alt="ball" />
                    <a> {team1} - {team2} </a>
                    <h6 className="mac_id_spacing">{mac_id} 
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                  <div className="shared-betslip-stat">
                    <p></p>
                    <p className="shared-betslip-tot-match">Total Matches</p>
                    <p className="shared-betslip-tot-match-cnt">{shared_match_cnt}</p>
                    <p></p>
                    <p className="shared-betslip-tot-match">Total Odd</p>
                    <p className="shared-betslip-tot-match-cnt">{shared_slip_total_odd}</p>
                  </div>

                </Card.Text>
              </Card.Body>
            </Card>
          </CardGroup>
          <CardGroup>
            <Card border="primary" style={{ height: '25rem' }}>
              <Card.Body>
                <Card.Title>Special title treatment</Card.Title>
                <Card.Text as="h6">
                  <img src={userpic} className="user-picture" alt="user" />
                  <a>  {username}</a>
                  <img src={like_icon} className="like-pic" alt="likebtn" />
                  <a>  {likecnt}</a>
                  <Button variant="primary" className="betslip-use">Use This Betslip</Button>
                  <p> </p>
                  <div className="shared-betslip">
                    <img src={logo} className="ball-logo" alt="ball" />
                    <a> {team1} - {team2} </a>
                    <h6 className="mac_id_spacing">{mac_id} 
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                  <div className="shared-betslip">
                    <img src={logo} className="ball-logo" alt="ball" />
                    <a> {team1} - {team2} </a>
                    <h6 className="mac_id_spacing">{mac_id} 
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                  <div className="shared-betslip-stat">
                    <p></p>
                    <p className="shared-betslip-tot-match">Total Matches</p>
                    <p className="shared-betslip-tot-match-cnt">{shared_match_cnt}</p>
                    <p></p>
                    <p className="shared-betslip-tot-match">Total Odd</p>
                    <p className="shared-betslip-tot-match-cnt">{shared_slip_total_odd}</p>
                  </div>

                </Card.Text>
              </Card.Body>
            </Card>
            <Card border="primary" style={{ height: '25rem' }}>
              <Card.Body>
                <Card.Title>Special title treatment</Card.Title>
                <Card.Text as="h6">
                  <img src={userpic} className="user-picture" alt="user" />
                  <a>  {username}</a>
                  <img src={like_icon} className="like-pic" alt="likebtn" />
                  <a>  {likecnt}</a>
                  <Button variant="primary" className="betslip-use">Use This Betslip</Button>
                  <p> </p>
                  <div className="shared-betslip">
                    <img src={logo} className="ball-logo" alt="ball" />
                    <a> {team1} - {team2} </a>
                    <h6 className="mac_id_spacing">{mac_id} 
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                  <div className="shared-betslip">
                    <img src={logo} className="ball-logo" alt="ball" />
                    <a> {team1} - {team2} </a>
                    <h6 className="mac_id_spacing">{mac_id} 
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                  <div className="shared-betslip-stat">
                    <p></p>
                    <p className="shared-betslip-tot-match">Total Matches</p>
                    <p className="shared-betslip-tot-match-cnt">{shared_match_cnt}</p>
                    <p></p>
                    <p className="shared-betslip-tot-match">Total Odd</p>
                    <p className="shared-betslip-tot-match-cnt">{shared_slip_total_odd}</p>
                  </div>

                </Card.Text>
              </Card.Body>
            </Card>
          </CardGroup>
        </div>
        <div className="betslipPanel">
          <div className="betslip-container">
            <div className="betslip-card">
              <CardGroup>
                <Card>
                  <Card.Header as="h5">MyBetslip</Card.Header>
                  <Card.Body>
                    <Card.Title>Special title treatment</Card.Title>
                    <Card.Text>
                      With supporting text below as a natural lead-in to additional content.
                    </Card.Text>
                    <Button variant="primary">Go somewhere</Button>
                  </Card.Body>
                </Card>
              </CardGroup>
              <Card>
                <Card.Body>
                  <Card.Title>Special title treatment</Card.Title>
                  <Card.Text>
                    With supporting text below as a natural lead-in to additional content.
                  </Card.Text>
                  <Button variant="primary">Go somewhere</Button>
                </Card.Body>
              </Card>
              <Card>
                <Card.Body>
                  <Card.Title>Special title treatment</Card.Title>
                  <Card.Text>
                    With supporting text below as a natural lead-in to additional content.
                  </Card.Text>
                  <Button variant="primary">Go somewhere</Button>
                </Card.Body>
              </Card>
              <Card>
                <Card.Body>
                  <Card.Title>Special title treatment</Card.Title>
                  <Card.Text>
                    With supporting text below as a natural lead-in to additional content.
                  </Card.Text>
                  <Button variant="primary">Go somewhere</Button>
                </Card.Body>
              </Card>
              <Card>
                <Card.Body>
                  <Card.Title>Special title treatment</Card.Title>
                  <Card.Text>
                    With supporting text below as a natural lead-in to additional content.
                  </Card.Text>
                  <Button variant="primary">Go somewhere</Button>
                </Card.Body>
              </Card>
            </div>
          </div>
        </div>
      </div>



    </body>

  );
}