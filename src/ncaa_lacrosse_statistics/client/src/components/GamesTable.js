import React, { useState, useEffect } from 'react';
import Table from 'react-bootstrap/Table';
import '../componentStyles/GamesTable.css';
import Container from 'react-bootstrap/Container';
import airforceLogo from '../pictures/airforce.png';
import armyLogo from '../pictures/army.webp';
import binghamtonLogo from '../pictures/binghamton.svg.png';
import bostonLogo from '../pictures/boston-u.jpeg';
import brownLogo from '../pictures/brown.svg.png';
import byrantLogo from '../pictures/Bryant.svg.png';
import bucknellLogo from '../pictures/Bucknell.svg.png';
import canisiusLogo from '../pictures/Canisius.svg.png';
import clevelandLogo from '../pictures/cleveland-state.svg';
import colgateLogo from '../pictures/colgate.png';
import cornellLogo from '../pictures/cornell.png';
import dartmouthLogo from '../pictures/Dartmouth.png';
import delawareLogo from '../pictures/delaware.png';
import denverLogo from '../pictures/denver.png';
import detroitLogo from '../pictures/detroit.png';
import drexelLogo from '../pictures/drexel.png';
import dukeLogo from '../pictures/duke.png';
import fairfieldLogo from '../pictures/fairfield.png';
import georgetownLogo from '../pictures/georgetown.png'; 
import hamptonLogo from '../pictures/hampton.png';
import hartfordLogo from '../pictures/hartford.png';
import harvardLogo from '../pictures/harvard.png';
import highpointLogo from '../pictures/highpoint.png';
import hobartLogo from '../pictures/hobart.png';
import hofstraLogo from '../pictures/hofstra.png';
import holycrossLogo from '../pictures/holycross.png';
import jacksonvilleLogo from '../pictures/jacksonville.png';
import hopkinsLogo from '../pictures/hopkins.png';
import lafayetteLogo from '../pictures/lafayette.png';
import lemoyneLogo from '../pictures/lemoyne.png';
import lindenwoodLogo from '../pictures/lindenwood.png';
import lehighLogo from '../pictures/lehigh.png';
import liuLogo from '../pictures/liu.png';
import loyolaLogo from '../pictures/loyola.png';
import manhattanLogo from '../pictures/manhattan.png';
import maristLogo from '../pictures/marist.png';
import marquetteLogo from '../pictures/marquette.png';
import marylandLogo from '../pictures/maryland.png';
import mercerLogo from '../pictures/mercer.png';
import michiganLogo from '../pictures/michigan.png';
import monmouthLogo from '../pictures/monmouth.png';
import mountLogo from '../pictures/mount.svg';
import navyLogo from '../pictures/navy.png';
import njitLogo from '../pictures/njit.png';
import uncLogo from '../pictures/unc.png';
import notredameLogo from '../pictures/notredame.png';
import osuLogo from '../pictures/osu.png';
import pennLogo from '../pictures/penn.png';
import pennstateLogo from '../pictures/pennstate.png';
import umassLogo from '../pictures/umass.png';
import princetonLogo from '../pictures/princeton.png';
import providenceLogo from '../pictures/providence.png';
import queensLogo from '../pictures/queens.png'; 
import richmondLogo from '../pictures/richmond.png';
import rmuLogo from '../pictures/rmu.png';
import quinnipiacLogo from '../pictures/quinnipiac.png';
import rutgersLogo from '../pictures/rutgers.png'
import sacredHeartLogo from '../pictures/sacredheart.png';
import sjuLogo from '../pictures/sju.png';
import sienaLogo from '../pictures/siena.png';
import stbonaventureLogo from '../pictures/stbonaventure.png';
import bellarmineLogo from '../pictures/bellarmine.png';
import saint_johnsLogo from '../pictures/saint_johns.png';
import stonybrookLogo from '../pictures/stony brook.png';
import syracuseLogo from '../pictures/syracuse.png';
import towsonLogo from '../pictures/towson.png';
import ualbanyLogo from '../pictures/albany.png';
import ulowellLogo from '../pictures/ulowell.png';
import utahLogo from '../pictures/utah.png';
import umbcLogo from '../pictures/umbc.png';
import vermontLogo from '../pictures/vermont.png';
import villanovaLogo from '../pictures/villanova.png';
import virginiaLogo from '../pictures/virginia.png';
import vmiLogo from '../pictures/vmi.png'
import wagnerLogo from '../pictures/wagner.png'
import yaleLogo from '../pictures/yale.png';
import merrimackLogo from '../pictures/merrimack.png';

import '../componentStyles/Logos.css';
const teamLogos = {
  "air force": airforceLogo,
  "army west point": armyLogo,
  "binghamton": binghamtonLogo,
  "boston u": bostonLogo,
  "brown": brownLogo,
  "bryant": byrantLogo,
  "bucknell": bucknellLogo,
  "canisius": canisiusLogo,
  "cleveland st": clevelandLogo,
  "colgate": colgateLogo,
  "cornell": cornellLogo,
  "dartmouth": dartmouthLogo,
  "delaware": delawareLogo,
  "denver": denverLogo,
  "detroit mercy": detroitLogo,
  "drexel": drexelLogo,
  "duke": dukeLogo,
  "fairfield": fairfieldLogo,
  "georgetown": georgetownLogo,
  "hampton": hamptonLogo,
  "harvard": harvardLogo,
  "hartford":hartfordLogo,
  "high point": highpointLogo,
  "hobart": hobartLogo,
  "hofstra": hofstraLogo,
  "holy cross":holycrossLogo,
  "jacksonville": jacksonvilleLogo,
  "johns hopkins": hopkinsLogo,
  "lafayette": lafayetteLogo,
  "le moyne": lemoyneLogo,
  "lindenwood": lindenwoodLogo,
  "lehigh": lehighLogo,
  "liu": liuLogo,
  "loyola maryland": loyolaLogo,
  "merrimack": merrimackLogo,
  "manhattan": manhattanLogo,
  "marist": maristLogo,
  "marquette": marquetteLogo,
  "maryland": marylandLogo,
  "mercer": mercerLogo,
  "massachusetts": umassLogo,
  "michigan": michiganLogo,
  "monmouth": monmouthLogo,
  "mount st marys": mountLogo,
  "navy": navyLogo,
  "njit": njitLogo,
  "north carolina": uncLogo,
  "umass": umassLogo,
  "notre dame": notredameLogo,
  "ohio st": osuLogo,
  "penn": pennLogo,
  "penn st": pennstateLogo,
  "umass": umassLogo,
  "princeton": princetonLogo,
  "providence": providenceLogo,
  "queens": queensLogo,
  "richmond": richmondLogo,
  "robert morris": rmuLogo,
  "quinnipiac": quinnipiacLogo,
  "rutgers": rutgersLogo,
  "sacred heart":sacredHeartLogo,
  "saint josephs": sjuLogo,
  "siena": sienaLogo,
  "st bonaventure": stbonaventureLogo,
  "bellarmine":bellarmineLogo,
  "st johns ": saint_johnsLogo,
  "stony brook": stonybrookLogo,
  "syracuse": syracuseLogo,
  "towson": towsonLogo,
  "ualbany": ualbanyLogo,
  "umass lowell": ulowellLogo,
  "utah": utahLogo,
  "umbc": umbcLogo,
  "vermont": vermontLogo,
  "villanova": villanovaLogo,
  "virginia": virginiaLogo,
  "vmi": vmiLogo,
  "wagner": wagnerLogo,
  "yale": yaleLogo
};

function GamesTable({ games }) {

  function formatDate(rawDate) {
    // Assuming rawDate is in the format 2102024
    const year = rawDate % 10000;
    const month = Math.floor(rawDate / 1000000);
    const day = Math.floor((rawDate % 1000000) / 10000);
    const date = new Date(year, month - 1, day);
    // Convert the date to a string in the format "Month Day, Year"
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  }

  return (
  <Container className="my-games-container" style={{ maxHeight: '800px', overflowY: 'auto' }}>
    <Table bordered hover striped responsive >
      <thead>
        <tr>
          <th>Date</th>
          <th>Team Name</th>
          <th>Opponent</th>
          <th className="result">Result</th>
          <th>OT</th>
          <th>Home</th>
          <th>Away</th>
          <th>Goals</th>
          <th>Assists</th>
          <th>Points</th>
          <th>Shots</th>
          <th>SOG</th>
          <th>GB</th>
          <th>TO</th>
          <th>CT</th>
          <th>Pen</th>
          <th>Saves</th>
          <th>FO_Won</th>
          <th>FOs_Taken</th>
          <th>Clear_Pct</th>
          <th>Man_Up_G</th>
          <th>Location</th>
          <th>Distance_Traveled</th>
         {/*  <th>Opp_Assists</th>
          <th>Opp_Points</th>
          <th>Opp_Shots</th>
          <th>Opp_SOG</th>
          <th>Opp_GB</th>
          <th>Opp_TO</th>
          <th>Opp_CT</th>
          <th>Opp_Pen</th>
          <th>Opp_Saves</th>
          <th>Opp_FO_Won</th>
          <th>Opp_FOs_Taken</th> 
          <th>Opp_Clear_Pct</th>
          <th>Opp_Man_Up_G</th> */}
        </tr>
      </thead>
      <tbody>
        {games.length > 0 ? (
          games.map((game, index) => (
            <tr key={index}>
              {/* Render table data for each attribute */}
              <td>{formatDate(game.Date)}</td>
              <td>
                <div className="opponent-info">
                <span>{game.Team_Name.charAt(0).toUpperCase() + game.Team_Name.slice(1)}</span>
                <img src={teamLogos[game.Team_Name]} alt={game.Team_Name} className="team-logo" />
                </div>
                </td>
              <td>
                <div className="opponent-info">
                <span>{game.Opponent.charAt(0).toUpperCase() + game.Opponent.slice(1)}</span>
                <img src={teamLogos[game.Opponent]} alt={game.Opponent} className="team-logo" />
                </div>
              </td>
              <td style={{ color: game.L === 1 ? '#FF6347' : '#32CD32' }}>{game.Result}</td>
              <td>{game.OT}</td>
              <td>{game.Home}</td>
              <td>{game.Away}</td>
              <td>{game.Goals}</td>
              <td>{game.Assists}</td>
              <td>{game.Points}</td>
              <td>{game.Shots}</td>
              <td>{game.SOG}</td>
              <td>{game.GB}</td>
              <td>{game.TO}</td>
              <td>{game.CT}</td>
              <td>{game.Pen}</td>
              <td>{game.Saves}</td>
              <td>{game.FO_Won}</td>
              <td>{game.FOs_Taken}</td>
              <td>{game.Clear_Pct}</td>
              <td>{game.Man_Up_G}</td>
              <td>{game.Location}</td>
              <td>{game.Distance_Traveled}</td>
            {/*  <td>{game.Opp_Assists}</td>
              <td>{game.Opp_Points}</td>
              <td>{game.Opp_Shots}</td>
              <td>{game.Opp_SOG}</td>
              <td>{game.Opp_GB}</td>
              <td>{game.Opp_TO}</td>
              <td>{game.Opp_CT}</td>
              <td>{game.Opp_Pen}</td>
              <td>{game.Opp_Saves}</td>
              <td>{game.Opp_FO_Won}</td>
              <td>{game.Opp_FOs_Taken}</td>
              <td>{game.Opp_Clear_Pct}</td>
              <td>{game.Opp_Man_Up_G}</td> */}
            </tr>
          ))
        ) : (
          <tr>
            <td colSpan="/* number of columns */">No games found</td>
          </tr>
        )}
      </tbody>
    </Table>
    </Container>
  );
}

export default GamesTable;
