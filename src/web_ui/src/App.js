import React from 'react';
import { Header } from './components/Header.js';
import { SensorDisplay } from './components/SensorDisplay.js';
import { Footer } from './components/Footer.js';
import logo from './logo.svg';
import './App.css';


function App() {
  return (    
    <div className="App">
      <Header />
      <SensorDisplay />
      <Footer />
    </div>
  );
}

export default App;
