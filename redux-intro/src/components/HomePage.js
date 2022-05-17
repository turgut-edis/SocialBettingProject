import React, { useState } from "react";
import Button from "react-bootstrap/Button";
import { Component } from "react";
import players from "./players";
import logo from './image/clipart442066.png'
import trash_icon from './image/trash-347.png'
import share_icon from './image/share-this-2600.png'
import "./csscomponents/homepage.css";



import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Switch,
} from "react-router-dom";
import { Card, CardGroup, Table } from "react-bootstrap";

var user = "dodo";
var team1 = "Team1";
var team2 = "Team2";
var mac_sonu = "2";
var odd = "2.55";
var mac_id = "5";
var mbn = "2";
var max_winning = "270";
var total_odd = "10.54";
var league_name = "League Name";

class HomePage extends Component {
  constructor(props) {
    super(props);
    this.state = { expandedRows: [] };
  }

  handleExpand = player => {
    let newExpandedRows = [...this.state.expandedRows];
    let allExpanded = this.state.allExpanded;
    let idxFound = newExpandedRows.findIndex(id => {
      return id === player.id;
    });

    if (idxFound > -1) {
      console.log("Collapsing " + player.firstName + " " + idxFound);
      newExpandedRows.splice(idxFound, 1);
    } else {
      console.log("Expanding " + player.firstName);
      newExpandedRows.push(player.id);
    }

    console.log("Expanded rows");
    console.log(newExpandedRows);

    this.setState({ expandedRows: [...newExpandedRows] });
  };

  isExpanded = player => {
    const idx = this.state.expandedRows.find(id => {
      return id === player.id;
    });

    return idx > -1;
  };

  expandAll = players => {
    console.log("ExpandedRows: " + this.state.expandedRows.length);
    console.log("Players:      " + players.length);
    if (this.state.expandedRows.length === players.length) {
      let newExpandedRows = [];
      this.setState({ expandedRows: [...newExpandedRows] });
      console.log("Collapsing all...");
    } else {
      let newExpandedRows = players.map(player => player.id);
      this.setState({ expandedRows: [...newExpandedRows] });
      console.log("Expanding all...");
      console.log("Expanded rows " + newExpandedRows.length);
    }
  };

  getRows = player => {
    let rows = [];
    const projects = player.projects || [];

    const firstRow = (
      <tr>
        <td>{player.id}</td>
        <td>{player.firstName}</td>
        <td>{player.lastName}</td>
        <td>{player.stats.weight}</td>
        <td>{player.stats.weight}</td>
        <td>{player.stats.weight}</td>
        <td>{player.stats.weight}</td>
        <td>{player.stats.weight}</td>
        <td>{player.stats.height}</td>
        <td><Button variant="primary" onClick={() => alert("Bet Added...")}></Button>
        </td>

        <td>
          {projects.length > 0 && (
            <button onClick={() => this.handleExpand(player)}>
              {this.isExpanded(player) ? "-" : "+"}
            </button>
          )}
        </td>
      </tr>
    );

    rows.push(firstRow);

    if (this.isExpanded(player) && projects.length > 0) {
      const projectRows = projects.map(project => (
        <tr className="player-details">
          <td className="player-details" />
          <td colspan="7" className="player-details">
            <br />
            <div>
              <div className="table-align">
                <Table responsive className="inner-table">
                  <thead>
                    <tr>
                      <th>FH/MR</th>
                      <th>Ratio</th>
                    </tr>
                  </thead>
                  <tbody striped="1">
                    <tr>
                      <td>0/0</td>
                      <td>3.0</td>
                    </tr>
                    <tr>
                      <td>0/X</td>
                      <td>3.0</td>
                    </tr>
                    <tr>
                      <td>0/1</td>
                      <td>3.0</td>
                    </tr>
                    <tr>
                      <td>1/0</td>
                      <td>3.0</td>
                    </tr>
                    <tr>
                      <td>1/X</td>
                      <td>3.0</td>
                    </tr>
                    <tr>
                      <td>1/1</td>
                      <td>3.0</td>
                    </tr>
                  </tbody>
                </Table>
              </div>
              <div className="table-align">
                <Table responsive className="inner-table">
                  <thead>
                    <tr>
                      <th>Goal Count</th>
                      <th>Ratio</th>
                    </tr>
                  </thead>
                  <tbody striped="1">
                    <tr>
                      <td>Over 2.5</td>
                      <td>2.1</td>
                    </tr>
                    <tr>
                      <td>Under 2.5</td>
                      <td>3.2</td>
                    </tr>
                  </tbody>
                </Table>
              </div>
              <div className="table-align">
                <Table responsive className="inner-table">
                  <thead>
                    <tr>
                      <th>Read Card Count</th>
                      <th>Ratio</th>
                    </tr>
                  </thead>
                  <tbody striped="1">
                    <tr>
                      <td>0</td>
                      <td>1.2</td>
                    </tr>
                    <tr>
                      <td>1</td>
                      <td>3.4</td>
                    </tr>
                    <tr>
                      <td>2</td>
                      <td>2.3</td>
                    </tr>
                    <tr>
                      <td>3</td>
                      <td>11</td>
                    </tr>
                  </tbody>
                </Table>
              </div>
              <div className="table-align">
                <Table responsive className="inner-table">
                  <thead>
                    <tr>
                      <th>Yellow Card Count</th>
                      <th>Ratio</th>
                    </tr>
                  </thead>
                  <tbody striped="1">
                    <tr>
                      <td>0</td>
                      <td>1.4</td>
                    </tr>
                    <tr>
                      <td>1</td>
                      <td>2.8</td>
                    </tr>
                    <tr>
                      <td>2</td>
                      <td>4.0</td>
                    </tr>
                    <tr>
                      <td>3</td>
                      <td>4.3</td>
                    </tr>
                    
                  </tbody>
                </Table>
              </div>
              <div className="table-align">
                <Table responsive className="inner-table">
                  <thead>
                    <tr>
                      <th>Corner Count</th>
                      <th>Ratio</th>
                    </tr>
                  </thead>
                  <tbody striped="1">
                    <tr>
                      <td>Over 7.5</td>
                      <td>4.1</td>
                    </tr>
                    <tr>
                      <td>Under 7.5</td>
                      <td>1.2</td>
                    </tr>
                  </tbody>
                </Table>
              </div>     
              <div className="attribute-value">{project.name}</div>
            </div>
            <br />
          </td>
        </tr>
      ));

      rows.push(projectRows);
    }

    return rows;
  };

  getPlayerTable = players => {
    const playerRows = players.map(player => {
      return this.getRows(player);
    });

    return (
      <div className="home-container">
        <nav class="navHomeTable">
          <a href="#all">All</a>
          <a href="#football">Football</a>
          <a href="#basketball">Basketball</a>
          <a href="#tennis">Tennis</a>
          <a href="#lol">LoL</a>
          <div class="animation start-home"></div>
        </nav>
        <div className="select-container">
          <select class="form-select" aria-label="Default select example">
            <option selected>Select League</option>
            <option value="1">One</option>
            <option value="2">Two</option>
            <option value="3">Three</option>
          </select>
          <select class="form-select" aria-label="Default select example">
            <option selected>Select MBN</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
          </select>
          <select class="form-select" aria-label="Default select example">
            <option selected>Sort By</option>
            <option value="1">Desc Ratio</option>
            <option value="2">Asc Ratio</option>
            <option value="3">Name</option>
          </select>
          <div class="input-group">
            <div class="form-outline">
              <input type="search" id="form1" class="form-control" placeholder="Search Match Name" />
            </div>
            <button type="button" class="btn btn-primary">
              <i class="fas fa-search">Search</i>
            </button>
          </div>
        </div>
        <div class="table-container">
          <span>{league_name}</span>
        </div>
        <table className="my-table table table">

          <tr>
            <th scope="col">Match ID</th>
            <th scope="col">Home</th>
            <th scope="col">Away</th>
            <th scope="col">1</th>
            <th scope="col">X</th>
            <th scope="col">2</th>
            <th scope="col">Over</th>
            <th scope="col">Under</th>
            <th scope="col">Date</th>
            <th scope="col">Bet</th>
            <th scope="col" onClick={() => this.expandAll(players)}>
              <button>
                {players.length === this.state.expandedRows.length ? "-" : "+"}
              </button>
            </th>
          </tr>
          {playerRows}
        </table>

        <div className="nav">
          <nav className="navbar navbar-expand-lg navbar-light fixed-top">
            <Link className="navbar-brand" to={"/"}>BETaBET</Link>
            <div className="collapse navbar-collapse" id="navbarTogglerDemo02">
              <ul className="navbar-nav">
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
                  <p>Funds:1500 TRY </p>
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

        <div className="betslip-container2">
          <div className="betslip-card">
            <CardGroup style={{ width: '26rem' }}>
              <Card>
                <Card.Header as="h5">MyBetslip</Card.Header>
                <Card.Body>
                  <div className="rightpanel-betslip">
                    <h6><img src={logo} className="ball-logo" alt="ball" /><span> {team1} - {team2} </span></h6>
                    <h6 className="mac_id_spacing">{mac_id}
                      <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                    </h6>
                  </div>
                </Card.Body>
              </Card>
            </CardGroup>
            <Card>
              <Card.Body>
                <div className="rightpanel-betslip">
                  <h6><img src={logo} className="ball-logo" alt="ball" /><span> {team1} - {team2} </span></h6>
                  <h6 className="mac_id_spacing">{mac_id}
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                  </h6>
                </div>
              </Card.Body>
            </Card>
            <Card>
              <Card.Body>
                <div className="rightpanel-betslip">
                  <h6><img src={logo} className="ball-logo" alt="ball" /><span> {team1} - {team2} </span></h6>
                  <h6 className="mac_id_spacing">{mac_id}
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                  </h6>
                </div>
              </Card.Body>
            </Card>
            <Card>
              <Card.Body>
                <div className="rightpanel-betslip">
                  <h6><img src={logo} className="ball-logo" alt="ball" /><span> {team1} - {team2} </span></h6>
                  <h6 className="mac_id_spacing">{mac_id}
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                  </h6>
                </div>
              </Card.Body>
            </Card>
            <Card>
              <Card.Body>
                <div className="rightpanel-betslip">
                  <h6><img src={logo} className="ball-logo" alt="ball" /><span> {team1} - {team2} </span></h6>
                  <h6 className="mac_id_spacing">{mac_id}
                    <span className="match-info-space">MS: {mac_sonu} Odd: {odd}</span>
                  </h6>
                </div>
              </Card.Body>
            </Card>
            <div className="betslip-checkout-card">
              <Card>
                <Card.Body>
                  <div className="rightpanel-checkout">
                    <h6 className="checkout">MBN: {mbn}</h6>
                    <h6 className="checkout">Max Winning: TRY{max_winning}</h6>
                  </div>
                  <div>
                    <h6>Total Odd: {total_odd}</h6>
                    <input id="amount_bet" type="text" className="input-lower" placeholder="Enter an amount..." />
                    <img src={trash_icon} className="lower-icon" alt="delete" onclick="trash()" />
                    <img src={share_icon} className="lower-icon" alt="share" onclick="share()" />
                    <Button variant="success" className="checkout-button" onclick="place_bet(amount_bet)">Place Bet</Button>
                  </div>
                </Card.Body>
              </Card>
            </div>
          </div>
        </div>

      </div>

    );
  };

  render() {
    return <div>{this.getPlayerTable(players)}</div>;
  }
}

export default HomePage;
