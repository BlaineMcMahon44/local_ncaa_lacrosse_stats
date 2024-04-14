import logo from '../lacrosse.png'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import '../componentStyles/Header.css';
import { Link } from 'react-router-dom';

function Header() {
    return (
        <Row>
            <Navbar navbar-expand-lg className="bg-body-tertiary nav-header bg-light">
                <Container fluid>
                    <Navbar.Brand className="d-flex align-items-center">
                        <img
                            alt=""
                            src={logo}
                            width="30"
                            height="30"
                            className="d-inline-block align-top"
                        />{' '}
                        <span className="ms-2">Lax Stat</span>
                        <div class="collapse navbar-collapse" id="navbarSupportedContent">
                            <ul class="navbar-nav mr-auto">
                            <li class="nav-item">
                                    <Link to="/" class="nav-link" href="#">Home</Link>
                                </li>
                                <li class="nav-item active">
                                    <Link to="/teams" class="nav-link" href="#">Teams</Link>
                                </li>
                                <li class="nav-item">
                                    <Link to="/games" class="nav-link" href="#">Games</Link>
                                </li>
                            </ul>
                        </div>
                    </Navbar.Brand>
                </Container>
            </Navbar>
        </Row>


    );
}

export default Header;