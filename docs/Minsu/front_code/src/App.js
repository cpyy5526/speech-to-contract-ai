import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Home from "./pages/Home";
import Recording from "./pages/Recording";
import Converting from "./pages/Converting";
import Download from "./pages/Contract_download";

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
