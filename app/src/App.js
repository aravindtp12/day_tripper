import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ChatInterface from './ChatInterface';
import LandingPage from './LandingPage';

function App() {
  return (
    <Router>
      <div className="App">
        <div className="chat-container">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/chat" element={<ChatInterface />} />
          </Routes>
          <div className="right-panel">
            {/* Right panel content will go here */}
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;