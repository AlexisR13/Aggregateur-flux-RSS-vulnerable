import axios from 'axios';
import {useEffect, useState} from 'react';
import FeedsList from '../FeedsList';
import Loader from '../Loader';

export default function FeedsListPannel() {
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
    <div>
        { Object.keys(fluxRSS).length===0 ?
        // Loading...
        <Loader/> :
        // Flux list
        <FeedsList fluxRSS={fluxRSS} isFavorite={isFavorite} setIsFavorite={setIsFavorite}/>
        }
    </div>
  );
}
