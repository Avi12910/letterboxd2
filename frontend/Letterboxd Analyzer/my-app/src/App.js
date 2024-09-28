import './App.css';
import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import UserHistory from './pages/UserHistory';
import { ChakraProvider } from '@chakra-ui/react'

const App = () => {
  return (
    <ChakraProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/letterboxd2" element={<UserHistory />} />
        </Routes>
      </BrowserRouter>
    </ChakraProvider>
  );
};

export default App;