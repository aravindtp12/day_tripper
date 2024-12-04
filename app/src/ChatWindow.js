// app/src/ChatWindow.js
import React from 'react';
import DatePicker from "react-datepicker";

const ChatWindow = ({ messages, input, setInput, handleSend, renderMessage, messagesEndRef, setShowChat }) => (
    <div className="chat-window">
        <button 
            className="back-button"
            onClick={() => setShowChat(false)}
        >
            Back
        </button>
        <div className="messages-container">
            {messages.map((msg, index) => renderMessage(msg, index))}
            <div ref={messagesEndRef} />
        </div>
        <div className="input-container">
            <input
                className="message-input"
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Type a message..."
            />
            <button className="send-button" onClick={handleSend}>
                Send
            </button>
        </div>
    </div>
);

export default ChatWindow;