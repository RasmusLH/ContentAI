import React from 'react';

const Contact: React.FC = () => {
  return (
    <div className="page-container">
      <h2 className="page-title">Get in Touch</h2>
      <div className="contact-grid">
        <div className="contact-item">
          <div className="contact-icon">
            <img src="/linkedin-icon.svg" alt="LinkedIn" />
          </div>
          <div className="contact-content">
            <h3>LinkedIn</h3>
            <p>Connect with me professionally and stay updated with my latest posts.</p>
            <a href="https://www.linkedin.com/in/rlha" className="contact-link linkedin">
              Connect on LinkedIn
            </a>
          </div>
        </div>
        
        <div className="contact-item">
          <div className="contact-icon">
            <img src="/github-icon.svg" alt="GitHub" />
          </div>
          <div className="contact-content">
            <h3>GitHub</h3>
            <p>Check out my open source projects and contributions.</p>
            <a href="https://github.com/RasmusLH" className="contact-link github">
              View Projects on GitHub
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;
