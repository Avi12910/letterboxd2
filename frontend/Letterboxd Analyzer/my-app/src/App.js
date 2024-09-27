import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect } from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import UserHistory from './pages/UserHistory';
import { ChakraProvider } from '@chakra-ui/react'

import axios from 'axios'

const App = () => {
  return (
    <ChakraProvider>
      <Router>
        <Routes>
          <Route path="/" element={<UserHistory />} />
        </Routes>
      </Router>
    </ChakraProvider>
  );
};

export default App;


// function UserForm({input, setInput, onUserFormSubmit}) {

//   return (
//       <form onSubmit={onUserFormSubmit}>
//           <label>
//               Enter Username: <input value={input} onChange = {(e) => setInput(e.target.value)} />
//           </label>
//           <button type="submit">Enter</button>
//           <p>Curret Input Value: {input}</p>
//       </form>
//   )
// } 

// function App() {

//     const [data, setData] = useState(null)
    
//     const [inputValue, setInputValue] = useState('')


//     // useEffect(() => {
//     //   axios.get('http://localhost:5000/hello/Avi')
//     //       .then(response => {
//     //         setData(response.data);
//     //       })
//     //       .catch(error => {
//     //         console.error("There was an error!", error)
//     //       });
//     // }, []);

//     function handleSubmit(event) {
//       event.preventDefault()

//       axios.get('http://localhost:5000/allfilms/' + inputValue)
//           .then(response => {
//             setData(response.data);
//           })
//           .catch(error => {
//             console.error("There was an error!", error)
//           })
//     }

//     return (
//       <div>
//           <h1>Data from Flask</h1>
//           <UserForm input={inputValue} 
//                     setInput={(e) => setInputValue(e)} 
//                     onUserFormSubmit={(e) => handleSubmit(e)}>          
//           </UserForm>
//           {data ? <p>{JSON.stringify(data.message, null, 2)}</p> : <p>Loading...</p>}
//       </div>
//     )



//   // return (
//   //   <div className="App">
//   //     <header className="App-header">
//   //       <img src={logo} className="App-logo" alt="logo" />
//   //       <p>
//   //         Edit <code>src/App.js</code> and save to reload.
//   //       </p>
//   //       <a
//   //         className="App-link"
//   //         href="https://reactjs.org"
//   //         target="_blank"
//   //         rel="noopener noreferrer"
//   //       >
//   //         Learn React
//   //       </a>
//   //     </header>
//   //   </div>
//   // );
// }

// export default App;
