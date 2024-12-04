import React from 'react';
import ChatInterface from './ChatInterface';

function App() {
  return (
    <div className="App">
      <div className="chat-container">
        <ChatInterface />
        <div className="right-panel">
          {/* Right panel content will go here */}
        </div>
      </div>
    </div>
  );
}

export default App;