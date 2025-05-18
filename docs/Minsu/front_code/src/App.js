// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./Login";
import Signup from "./Signup";
import Home from "./Home";
import Recording from "./Recording"
import Converting from "./Converting";
import Download from "./Contract_download"

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} /> 
        <Route path="/signup" element={<Signup />} />
        <Route path="/home" element={<Home />} />
        <Route path="/recording" element={<Recording />} />
        <Route path="/converting" element={<Converting />} />
        <Route path="/download" element={<Download />} />
      </Routes>
    </Router>
  );
}

export default App;