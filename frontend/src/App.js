import './App.css';
import axios from 'axios';
import {useEffect, useState} from 'react';

function App() {
  const [fluxRSS, setFluxRSS] = useState({})
  useEffect(() => {
    axios.get('http://localhost:5000').then((response) => {
      setFluxRSS(response.data);
    })
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <h1>
          Flux RSS disponibles :
        </h1>
        <ul>
          {Object.keys(fluxRSS).map((name) => <li>{name}</li>)}
        </ul>
      </header>
    </div>
  );
}

export default App;
