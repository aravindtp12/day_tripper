import * as React from 'react';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const API_URL = 'http://localhost:8000/api';

const ChatInterface = () => {
    const [messages, setMessages] = React.useState([]);
    const [input, setInput] = React.useState('');
    const [dateRange, setDateRange] = React.useState([null, null]);
    const messagesEndRef = React.useRef(null);

    React.useEffect(() => {
        setMessages([{
            text: "Where do you want to travel to?",
            sender: 'bot',
            type: 'text'
        }]);
    }, []);

    const handleSend = () => {
        if (input.trim()) {
            setMessages(prev => [...prev, { 
                text: input, 
                sender: 'user', 
                type: 'text' 
            }]);

            setInput('');

            setTimeout(() => {
                setMessages(prev => [...prev, 
                    { 
                        text: "When would you like to travel?", 
                        sender: 'bot',
                        type: 'text'
                    },
                    {
                        sender: 'bot',
                        type: 'date-picker'
                    }
                ]);
            }, 1000);
        }
    };

    const saveTravelPlan = async (destination, startDate, endDate) => {
        try {
            const response = await fetch(`${API_URL}/chat/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    destination: destination,
                    start_date: startDate.toISOString().split('T')[0],
                    end_date: endDate.toISOString().split('T')[0],
                }),
            });
            
            const data = await response.json();
            console.log('Travel plan saved:', data);
            
        } catch (error) {
            console.error('Error saving travel plan:', error);
        }
    };

    const handleDateSelection = (update) => {
        setDateRange(update);
        
        if (update[0] && update[1]) {
            const dateMessage = `${update[0].toLocaleDateString()} - ${update[1].toLocaleDateString()}`;
            setMessages(prev => [...prev, { 
                text: dateMessage, 
                sender: 'user', 
                type: 'text' 
            }]);

            saveTravelPlan(messages[1].text, update[0], update[1]);

            setTimeout(() => {
                setMessages(prev => [...prev, { 
                    text: `Great! Let me help you plan your trip from ${update[0].toLocaleDateString()} to ${update[1].toLocaleDateString()}.`, 
                    sender: 'bot',
                    type: 'text'
                }]);
            }, 1000);
        }
    };

    const renderMessage = (msg, index) => {
        if (msg.type === 'text') {
            return (
                <div 
                    key={index} 
                    className={`message ${msg.sender === 'user' ? 'user-message' : 'bot-message'}`}
                >
                    {msg.text}
                </div>
            );
        } else if (msg.type === 'date-picker') {
            return (
                <div key={index} className="date-picker-container">
                    <DatePicker
                        selected={dateRange[0]}
                        onChange={(dates) => handleDateSelection(dates)}
                        startDate={dateRange[0]}
                        endDate={dateRange[1]}
                        selectsRange
                        inline
                        minDate={new Date()}
                    />
                </div>
            );
        }
        return null;
    };

    return (
        <div className="chat-window">
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
};

export default ChatInterface;