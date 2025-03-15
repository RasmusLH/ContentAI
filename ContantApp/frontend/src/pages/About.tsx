import React from 'react';

const About: React.FC = () => {
  return (
    <div className="page-container">
      <div className="about-box">
        <h2 className="page-title">About the Creator</h2>
        <div className="about-content">
          <p>
            Hi! I'm a passionate hobby developer with a keen interest in AI and technologies.
          </p>
          <p>
            I created Linkedinker as a sideproject as part of learning AI development but hopefully 
            someone out there can actually use it.
          </p>
        </div>
      </div>
    </div>
  );
};

export default About;
