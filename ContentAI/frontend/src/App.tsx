import "./App.css";
import React from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
import PostGenerator from "./components/PostGenerator";

function App() {
  return (
    <div className="app-container">
      <Header />
      <main className="main-content">
        <PostGenerator />
      </main>
      <Footer />
    </div>
  );
}

export default App;
