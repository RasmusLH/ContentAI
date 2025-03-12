import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  return (
    <div className="home-container">
      <section className="hero">
        <h1>Welcome to Linkedinker</h1>
        <p>Generate professional and engaging LinkedIn posts in minutes</p>
        <Link to="/create" className="cta-button">Start Creating</Link>
      </section>
      
      <section className="steps-section">
        <h2>How It Works</h2>
        <div className="steps-container">
          <div className="step-item">
            <div className="step-number">1</div>
            <div className="step-content">
              <h3>Choose Template</h3>
              <p>Select from professionally crafted templates for tech insights, startup stories, product launches, or industry updates.</p>
            </div>
          </div>

          <div className="step-item">
            <div className="step-number">2</div>
            <div className="step-content">
              <h3>Main Message</h3>
              <p>Describe your core message or objective. What key point do you want to communicate to your audience?</p>
            </div>
          </div>

          <div className="step-item">
            <div className="step-number">3</div>
            <div className="step-content">
              <h3>Add Context</h3>
              <p>Provide relevant details about your company, audience, or industry. Upload supporting documents for more tailored content.</p>
            </div>
          </div>

          <div className="step-item">
            <div className="step-number">4</div>
            <div className="step-content">
              <h3>Generate!</h3>
              <p>Let our AI create an engaging post that resonates with your LinkedIn audience.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
