import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Header: React.FC = () => {
  const { user, logout } = useAuth();
  
  return (
    <header className="app-header">
      <div className="header-content">
        <div className="header-logo">
          <h1><span>Linkedinker</span></h1>
        </div>
        <nav className="header-nav">
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/create">Create</Link></li>
            <li><Link to="/posts">Posts</Link></li>
            <li><Link to="/about">About</Link></li>
            <li><Link to="/contact">Contact</Link></li>
            <li>
              {user ? (
                <button onClick={logout} className="auth-button">Logout</button>
              ) : (
                <Link to="/login" className="auth-button">Login</Link>
              )}
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
