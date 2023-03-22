import axios from 'axios';
import {useEffect, useState} from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  const [fluxRSS, setFluxRSS] = useState({})
  useEffect(() => {
    axios.get('http://localhost:5000').then((response) => {
      setFluxRSS(response.data);
    })
  }, [])

  return (
    <>
      <h1>Flux RSS disponibles :</h1>
      <ul>
        {Object.keys(fluxRSS).map((name) => 
          <li key={name}>
            <Link to={'feed/'+name}>{name}</Link>
          </li>
        )}
      </ul>
    </>
  );
}

export default HomePage;
