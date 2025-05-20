import { useState } from "react";
import Login from "./pages/Login.jsx";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home.jsx";
import Learning from "./pages/Learning.jsx";
import Practice from "./pages/Practice.jsx";
import { ThemeProvider } from "./components/ThemeContext.jsx";
import AboutUs from "./pages/AboutUs.jsx";

function App() {
  return (
    <ThemeProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/learn" element={<Learning />} />
          <Route path="/practice" element={<Practice />} />
          <Route path="/about" element={<AboutUs />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
