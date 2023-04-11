import axios from 'axios';
import {useEffect, useState} from 'react';
import { useSelector } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom';

function HomePage() {
  const [fluxRSS, setFluxRSS] = useState({});
  const [isStarFull, setIsStarFull] = useState([]);
  const authCookie = useSelector((state) => state.authCookie.value);
  const navigate = useNavigate();

  // Get flux RSS list from backend
  useEffect(() => {
    axios.get('http://localhost:5000')
    .then((response) => {
      setFluxRSS(response.data);
      setIsStarFull(Object.keys(response.data).map(() => false));
    })
  }, [])

  // Update which flux are marked as favorite (star is full)
  function updateIsStarFull(idx) {
    // Ask user to authenticated to see its favorites
    if (!authCookie) {
      navigate('/connexion');
    }
    else {
      const newArray = [...isStarFull];
      newArray[idx] = !newArray[idx];
      setIsStarFull(newArray);
    }
  }

  return (
    <>
      <h1 className='text-3xl pb-5'>Flux RSS disponibles :</h1>
      { Object.keys(fluxRSS).length===0 ?
      <div className='flex flex-col items-center w-full mt-10'>
        <div className='border rounded-full w-10 h-10 border-t-orange-700 animate-spin mb-4'/>
        <p>Veuillez réessayer ultérieurement...</p>
      </div> :
      <div>
        <ul className='list-inside'>
          {Object.keys(fluxRSS).map((name, idx) => 
            <li key={name}>
              <button onClick={() => updateIsStarFull(idx)}>{isStarFull[idx] ? '★' : '☆'}</button>
              <Link to={'feed/'+name} className='ml-4 text-blue-700 underline'>
                {name}
              </Link>
            </li>
          )}
        </ul>
      </div>
      }
    </>
  );
}

export default HomePage;
