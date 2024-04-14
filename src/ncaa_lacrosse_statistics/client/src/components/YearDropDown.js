import { useState } from "react";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Container from 'react-bootstrap/Container';
import '../componentStyles/YearDropDown.css';
function YearDropDown(props) {
    function handleYearChange(event) {
        props.onYearChange(event.target.value);
    }
    return (
        <Col lg={6} sm={12} md={12}>
            <Form.Label htmlFor="yearSelect" style={{marginLeft: '17%', marginTop:'1%'}}>Select Year:</Form.Label  >
            <Form.Select className="year-dropdown" id="yearSelect" value={props.selectedYear} onChange={handleYearChange}>
                <option value="2024">2024</option>
                <option value="2023">2023</option>
                <option value="2022">2022</option>
                <option value="2021">2021</option>
                <option value="2020">2020</option>
                <option value="2019">2019</option>
                <option value="2018">2018</option>
            </Form.Select>
        </Col>
    );
}

export default YearDropDown;