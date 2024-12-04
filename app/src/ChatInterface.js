import React, { useState, useRef, useEffect } from 'react';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const API_URL = 'http://localhost:8000/api/chat/';

const ChatInterface = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [destination, setDestination] = useState('');
    const [dateRange, setDateRange] = useState([null, null]);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        setMessages([{
            text: "Where do you want to travel to?",
            sender: 'bot',
            type: 'text'
        }]);
    }, []);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = () => {
        if (input.trim()) {
            setMessages(prev => [...prev, { 
                text: input, 
                sender: 'user', 
                type: 'text' 
            }]);

            setDestination(input);
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
            const response = await fetch(API_URL, {
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
            console.log('Response from backend:', data);

            if (data.status === 'success' && data.recommendations) {
                setMessages(prev => [...prev, { 
                    text: data.recommendations, 
                    sender: 'bot',
                    type: 'text'
                }]);
            } else {
                throw new Error('No recommendations received');
            }
            
        } catch (error) {
            console.error('Error in saveTravelPlan:', error);
            setMessages(prev => [...prev, { 
                text: "Sorry, I encountered an error while generating recommendations.", 
                sender: 'bot',
                type: 'text'
            }]);
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

            if (destination) {
                setMessages(prev => [...prev, { 
                    text: "Generating travel recommendations... This might take a minute.", 
                    sender: 'bot',
                    type: 'text'
                }]);

                saveTravelPlan(destination, update[0], update[1]);
            } else {
                console.error('Destination not set');
                setMessages(prev => [...prev, { 
                    text: "Sorry, I couldn't find your destination. Please try again.", 
                    sender: 'bot',
                    type: 'text'
                }]);
            }
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