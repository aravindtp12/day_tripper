// app/src/LandingPage.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css';

const LandingPage = () => {
    const navigate = useNavigate();

    return (
        <div className="landing-page">
            <div className="landing-left">
                <img 
                    src="/landing_image.jpeg" 
                    alt="Travel Planning" 
                    className="landing-image"
                />
            </div>
            <div className="landing-right">
                <div className="action-buttons">
                    <button className="action-button">
                        <span className="plus-icon">+</span>
                        Create Itinerary
                    </button>
                    <button className="action-button">
                        Load Itinerary
                    </button>
                </div>
                <button 
                    className="continue-button"
                    onClick={() => navigate('/chat')}
                >
                    Continue
                </button>
            </div>
        </div>
    );
};

export default LandingPage;