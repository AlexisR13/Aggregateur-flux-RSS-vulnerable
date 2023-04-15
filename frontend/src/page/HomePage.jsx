import axios from 'axios';
import {useEffect, useState} from 'react';
import AddFluxForm from '../components/AddFluxForm';
import FluxList from '../components/FluxList';

function HomePage() {
  const [fluxRSS, setFluxRSS] = useState({});
  const [isFavorite, setIsFavorite] = useState([]);

  // Get flux RSS list from backend
  useEffect(() => {
    axios.get('/')
    .then((response) => {
      setFluxRSS(response.data);
      setIsFavorite(Object.keys(response.data).map(() => false));
    })
  }, [])

  return (
    <>
      <div>
        <h1 className='text-3xl pb-5'>Flux RSS disponibles :</h1>
        { Object.keys(fluxRSS).length===0 ?
        // Loading...
        <div className='flex flex-col items-center w-full mt-10'>
          <div className='border rounded-full w-10 h-10 border-t-orange-700 animate-spin mb-4'/>
          <p>Veuillez réessayer ultérieurement...</p>
        </div> :
        // Flux list
        <FluxList fluxRSS={fluxRSS} isFavorite={isFavorite} setIsFavorite={setIsFavorite}/>
        }
      </div>
      <AddFluxForm/>
    </>
  );
}

export default HomePage;
