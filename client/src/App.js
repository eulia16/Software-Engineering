import './App.css';
import React from 'react';

import { ThemeProvider, createMuiTheme } from '@mui/material/styles';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Layout from './layout';
import Home from './pages/home';
import CssBaseline from '@mui/material/CssBaseline';
import Login from './pages/login';


const theme = createMuiTheme({
  palette: {
    background: {
      default: '#eeeeee'
    },
    secondary: {
      main: '#000000'
    },
    primary: {
      main: '#01579b'
    },
    login: {
      main: '#1976d2'
    },
    latency: {
      main: '#01579b'
    }
  }
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline/>
    <div className="App">
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Login />} />
        </Route>
        <Route path="/home" element={<Layout />}>
          <Route index element={<Home />} />
        </Route>
      </Routes>
    </BrowserRouter>
    <br/>
    </div>
    </ThemeProvider>
    
  );
}

export default App;
