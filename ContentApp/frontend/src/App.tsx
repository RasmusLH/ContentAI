import "./styles/index.css";
import React, { Suspense } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Create from "./pages/Create";
import About from "./pages/About";
import Contact from "./pages/Contact";
import { GoogleOAuthProvider } from '@react-oauth/google';
import Login from './pages/Login';
import ProtectedRoute from './components/ProtectedRoute';
import Posts from './pages/Posts';
import { NotificationProvider } from './contexts/NotificationContext';

class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('App Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <div>Something went wrong. Please refresh the page.</div>;
    }
    return this.props.children;
  }
}

function App() {
  return (
    <React.StrictMode>
      <ErrorBoundary>
        <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID || ''}>
          <AuthProvider>
            <NotificationProvider>
              <Suspense fallback={<div>Loading...</div>}>
                <Router>
                  <div className="app-container">
                    <Header />
                    <main className="main-content">
                      <Routes>
                        <Route path="/login" element={<Login />} />
                        <Route path="/" element={<Home />} />
                        <Route path="/create" element={<Create />} />
                        <Route 
                          path="/posts" 
                          element={
                            <ProtectedRoute>
                              <Posts />
                            </ProtectedRoute>
                          } 
                        />
                        <Route path="/about" element={<About />} />
                        <Route path="/contact" element={<Contact />} />
                      </Routes>
                    </main>
                    <Footer />
                  </div>
                </Router>
              </Suspense>
            </NotificationProvider>
          </AuthProvider>
        </GoogleOAuthProvider>
      </ErrorBoundary>
    </React.StrictMode>
  );
}

export default App;
