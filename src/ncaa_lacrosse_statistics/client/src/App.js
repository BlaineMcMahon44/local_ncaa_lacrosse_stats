import './App.css';
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import YearDropDown from './components/YearDropDown';
import TeamsTable from './components/TeamsTable';
import GamesTable from './components/GamesTable';
import ScheduleTable from './components/ScheduleTable';
import TeamDropDown from './components/TeamDropDown';
import { Button } from 'react-bootstrap';
import Row from 'react-bootstrap/Row';
import Accordion from 'react-bootstrap/Accordion';
import { saveAs } from 'file-saver';
import RecentGamesTable from './components/RecentGamesTable';
import './componentStyles/HomePage.css';

function App() {
  const currentDate = new Date();
  const currentYear = currentDate.getFullYear().toString();
  const [teams, setTeams] = useState([]);
  const [selectedYear, setSelectedYear] = useState(currentYear);
  const [games, setGames] = useState([]);
  const [teamsNames, setTeamsNames] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState('');
  const [schedule, setSchedule] = useState([]);
  const [results, setResults] = useState([]);

  function handleYearChange(year) {
    setSelectedYear(year);
  }

  function handleTeamNameChange(teamName) {
    setSelectedTeam(teamName)
  }

  const TeamsPage = () => {
    const handleExportToCSV = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/teams/csv');
        if (!response.ok) {
          throw new Error('Failed to export CSV');
        }
        const blob = await response.blob();
        saveAs(blob, 'teams.csv'); // Save the blob as a file named 'teams.csv'
      } catch (error) {
        console.error('Error exporting CSV:', error);
      }
    };

    return (
      <div>
        <Accordion defaultActiveKey="0">
          <Accordion.Item eventKey="0">
            <Accordion.Header>Cumulative Team Statistics</Accordion.Header>
            <Accordion.Body>
              Statistics totals for each team over all of the games they've played in a given season.
              There is also an option to export the given stats to a CSV file.
            </Accordion.Body>
          </Accordion.Item>
        </Accordion>
        <Row>
          <YearDropDown selectedYear={selectedYear} onYearChange={handleYearChange}></YearDropDown>
          <TeamDropDown teamNames={teamsNames} onTeamChange={handleTeamNameChange} selectedTeam={selectedTeam} />
        </Row>

        <TeamsTable teams={teams} />
        <div className="d-flex justify-content-end" style={{ margin: '20px' }}>
          <Button onClick={handleExportToCSV}>Download CSV</Button>
        </div>
        {/* Add the export to CSV button */}

      </div>
    );
  }

  const GamesPage = () => {
    const handleExportGamesToCSV = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/games/csv');
        if (!response.ok) {
          throw new Error('Failed to export CSV');
        }
        const blob = await response.blob();
        saveAs(blob, 'games.csv'); // Save the blob as a file named 'teams.csv'
      } catch (error) {
        console.error('Error exporting CSV:', error);
      }
    };

    return (
      <div>
        <Accordion defaultActiveKey="0">
          <Accordion.Item eventKey="0">
            <Accordion.Header>Game By Game Statistics</Accordion.Header>
            <Accordion.Body>
              Results and game statistics for each game played throughout the season.
              There is also an option to export the given stats to a CSV file at the bottom of the page.
            </Accordion.Body>
          </Accordion.Item>
        </Accordion>
        <Row>
          <YearDropDown selectedYear={selectedYear} onYearChange={handleYearChange}></YearDropDown>
          <TeamDropDown teamNames={teamsNames} onTeamChange={handleTeamNameChange} selectedTeam={selectedTeam} />
        </Row>
        <GamesTable games={games} />
        <div className="d-flex justify-content-end" style={{ margin: '20px' }}>
          <Button onClick={handleExportGamesToCSV}>Download CSV</Button>
        </div>
      </div>
    );
  };

  useEffect(() => {
    const fetchSchedule = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const scheduleData = await response.json();
        console.log(scheduleData);
        setSchedule(scheduleData);
      } catch (error) {
        console.error('Error fetching schedule:', error);
      }
    };

    fetchSchedule();
  }, []); // Empty dependency array means this effect runs once on mount  

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/results`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const resultsData = await response.json();
        console.log(resultsData);
        setResults(resultsData);
      } catch (error) {
        console.error('Error fetching schedule:', error);
      }
    };

    fetchResults();
  }, []); // Empty dependency array means this effect runs once on mount 

  useEffect(() => {
    // Function to fetch teams data
    const fetchTeams = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/teams?year=${selectedYear}&team=${selectedTeam}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const teamsData = await response.json();
        console.log(teamsData);
        setTeams(teamsData);
      } catch (error) {
        console.error('Error fetching teams:', error);
      }
    };

    // Call fetchTeams function
    fetchTeams();
  }, [selectedYear, selectedTeam]); // Trigger fetchTeams when selectedYear changes


  useEffect(() => {
    const fetchGames = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/games?year=${selectedYear}&team=${selectedTeam}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const gamesData = await response.json();
        setGames(gamesData);
        console.log(gamesData);
      } catch (error) {
        console.error('Error fetching games:', error);
      }
    };

    fetchGames();
  }, [selectedYear, selectedTeam]); // Include selectedYear in the dependency array

  useEffect(() => {
    // Function to fetch teams data
    const fetchTeamsNames = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/teams/names?year=${selectedYear}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const teamsData = await response.json();
        console.log(teamsNames);
        setTeamsNames(teamsData);
      } catch (error) {
        console.error('Error fetching teams:', error);
      }
    };

    fetchTeamsNames();
  }, [selectedYear]); // Include selectedYear in the dependency array

  const HomePage = () => (
    <div>
      <h3>Schedule</h3>
      <ScheduleTable schedule={schedule} />
      <h3>Results</h3>
      {results.length > 0 ? (
        <RecentGamesTable results={Object.values(results)} />

      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
  return (
    <Router>
      <div>
        <Header />
        <Routes>
          <Route path="/" element={<HomePage schedule={schedule} results={results} />} />
          <Route path="/teams" element={<TeamsPage />} />
          <Route path="/games" element={<GamesPage />} />
        </Routes>
      </div>
    </Router>
  );
}
export default App;