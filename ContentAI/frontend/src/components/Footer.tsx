import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="app-footer">
      <div className="footer-content">
        <div className="footer-section">
          <h3>ContentAI</h3>
          <p>Empowering your social media presence with AI</p>
        </div>
        <div className="footer-section">
          <h4>Quick Links</h4>
          <ul>
            <li><a href="/privacy">Privacy Policy</a></li>
            <li><a href="/terms">Terms of Service</a></li>
          </ul>
        </div>
        <div className="footer-section">
          <p>&copy; {new Date().getFullYear()} ContentAI. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
