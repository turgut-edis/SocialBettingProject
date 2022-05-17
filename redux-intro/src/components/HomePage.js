import React, { useState } from "react";
import Form from "react-bootstrap/Form";
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
import { Card, CardGroup, Tab } from "react-bootstrap";

var user = "dodo";
var username = "Dodo";
var likecnt = "10";
var team1 = "Team1";
var team2 = "Team2";
var mac_sonu = "2";
var odd = "2.55";
var mac_id = "5";
var shared_match_cnt = "2";
var shared_slip_total_odd = "90.00";
var comment_like_cnt = "3";
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
    console.log("ExapndedRows: " + this.state.expandedRows.length);
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
        <td>{player.firstName}</td>
        <td>{player.lastName}</td>
        <td>{player.team}</td>
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
          <td colspan="3" className="player-details">
            <br />
            <div className="attribute">
              <div className="attribute-name">Toggle Here: </div>
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
        <table className="my-table">
          
          <tr>
            <th>Firstname</th>
            <th>Lastname</th>
            <th>Team</th>
            <th onClick={() => this.expandAll(players)}>
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
          asdasdfasfas
        </div>

      </div>

    );
  };

  render() {
    return <div>{this.getPlayerTable(players)}</div>;
  }
}

export default HomePage;
