import { useState } from "react";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Container from 'react-bootstrap/Container';
import '../componentStyles/YearDropDown.css';
import '../componentStyles/TeamDropDown.css'
function TeamDropDown(props) {
    function handleTeamChange(event) {
        props.onTeamChange(event.target.value);
    }
    return (
        <Col lg={6} sm={12} md={12}>
            <Form.Label htmlFor="teamSelect" style={{marginTop:'1%'}}>Select Team:</Form.Label>
            <Form.Select className="year-dropdown custom-margin" id="teamSelect" onChange={handleTeamChange} value={props.selectedTeam}>
            {props.teamNames.map((teamName, index) => (
                <option key={index} value={teamName}>{teamName}</option>
            ))}
            </Form.Select>
        </Col>
);
}

export default TeamDropDown;