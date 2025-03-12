import React from 'react';

const Contact: React.FC = () => {
  return (
    <div className="contact-container">
      <h2>Get in Touch</h2>
      <div className="contact-links">
        <div className="contact-item">
          <h3>LinkedIn</h3>
          <a href="https://www.linkedin.com/in/rlha" className="social-link linkedin">
            Connect on LinkedIn
          </a>
        </div>
        
        <div className="contact-item">
          <h3>GitHub</h3>
          <a href="https://github.com/RasmusLH" className="social-link github">
            View Projects on GitHub
          </a>
        </div>
      </div>
    </div>
  );
};

export default Contact;
