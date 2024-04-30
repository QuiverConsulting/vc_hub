import React from 'react';
import {  Routes, Route } from 'react-router-dom'; // Import BrowserRouter, Routes, and Route
import LandingPage from './components/pages/LandingPage';
import AboutPage from './components/pages/AboutPage';

const AppRoutes: React.FC = () => {
  return (
      <Routes>
        <Route path="/" element={<LandingPage />} /> 
        <Route path="/about" element={<AboutPage />} /> 
      </Routes>
  );
};

export default AppRoutes;