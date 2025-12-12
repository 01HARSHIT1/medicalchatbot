import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./components/Home";
import Logo1 from "./components/Logo1";
import Logo2 from "./components/Logo2";
import Logo3 from "./components/Logo3";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/logo1" element={<Logo1 />} />
        <Route path="/logo2" element={<Logo2 />} />
        <Route path="/logo3" element={<Logo3 />} />
      </Routes>
    </Router>
  );
};

export default App;

