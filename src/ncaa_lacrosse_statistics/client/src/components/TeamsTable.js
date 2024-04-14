import React from 'react';
import Container from 'react-bootstrap/Container';
import Table from 'react-bootstrap/Table';
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
import stjohnsLogo from '../pictures/stjohns.png'; 
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

import '../componentStyles/TeamsTable.css'
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
    "hartford":hartfordLogo,
    "hampton": hamptonLogo,
    "harvard": harvardLogo,
    "high point": highpointLogo,
    "hobart": hobartLogo,
    "hofstra": hofstraLogo,
    "holy cross": holycrossLogo,
    "jacksonville": jacksonvilleLogo,
    "johns hopkins": hopkinsLogo,
    "lafayette": lafayetteLogo,
    "le moyne": lemoyneLogo,
    "lindenwood": lindenwoodLogo,
    "lehigh": lehighLogo,
    "liu": liuLogo,
    "loyola maryland": loyolaLogo,
    "manhattan": manhattanLogo,
    "marist": maristLogo,
    "marquette": marquetteLogo,
    "maryland": marylandLogo,
    "mercer": mercerLogo,
    "merrimack": merrimackLogo,
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
    "sacred heart": sacredHeartLogo,
    "saint josephs": sjuLogo,
    "siena": sienaLogo,
    "st bonaventure": stbonaventureLogo,
    "bellarmine": bellarmineLogo,
    "st johns ": stjohnsLogo,
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
function TeamsTable({ teams }) {
    return (
        <Container className="teams-table-wrapper">
            <Table bordered hover striped size="sm" responsive style={{ maxHeight: '800px', overflowY: 'auto' }}>
                <thead>
                    <tr>
                        <th>Team Logo</th>
                        <th>Teams</th>
                        {teams.length > 0 &&
                            Object.keys(teams[0]).map((attribute) => (
                                attribute !== 'Id' &&
                                attribute !== 'Year' &&
                                attribute !== 'Team_Name' && (
                                    <th key={attribute}>{attribute}</th>
                                )
                            ))}
                        {/* Add more table headers for each attribute */}
                    </tr>
                </thead>
                <tbody>
                    {teams.map((team, index) => (
                        <tr key={index}>
                            {index === 0 || team.Team_Name !== teams[index - 1].Team_Name ? (
                                <>
                                    <td>
                                        <img
                                            src={teamLogos[team.Team_Name]}
                                            alt={team.Team_Name}
                                            className="team-logo"
                                        />
                                    </td>
                                    <td>{team.Team_Name}</td>
                                </>
                            ) : (
                                <>
                                    <td></td>
                                    <td></td>
                                </>
                            )}
                            {Object.keys(team).map((key) => (
                                key !== 'Id' &&
                                key !== 'Year' &&
                                key !== 'Team_Name' && <td key={key}>{team[key]}</td>
                            ))}
                            {/* Render more table data cells for each attribute */}
                        </tr>
                    ))}
                </tbody>
            </Table>
        </Container>
    );
}


export default TeamsTable;
