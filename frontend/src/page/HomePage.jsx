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
      <h1 className='text-3xl pb-5'>Flux RSS disponibles :</h1>
      <ul className='list-disc list-inside'>
        {Object.keys(fluxRSS).map((name) => 
          <li key={name}>
            <Link to={'feed/'+name} className='text-blue-700 underline'>
              {name}
            </Link>
          </li>
        )}
      </ul>
    </>
  );
}

export default HomePage;
